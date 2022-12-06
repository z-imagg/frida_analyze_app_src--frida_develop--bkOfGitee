#ref: https://www.anquanke.com/post/id/177597
from __future__ import print_function
import frida
from frida_tools.application import Reactor
import threading

class Application(object):
    def __init__(self):
        self._stop_requested = threading.Event()
        self._reactor = Reactor(run_until_return=lambda reactor: self._stop_requested.wait())

        self._device = frida.get_local_device()
        self._sessions = set()

        self._device.on("spawn-added", lambda child: self._reactor.schedule(lambda: self._on_delivered(child)))
    #     ValueError: Device does not have a signal named 'delivered', it only has: 'spawn-added', 'spawn-removed', 'child-added', 'child-removed', 'process-crashed', 'output', 'uninjected', 'lost'

    def run(self):
        self._reactor.schedule(lambda: self._start())
        self._reactor.run()

    def _start(self):
        # argv = ["/bin/sh", "-c", "cat /etc/hosts"]
        argv = ["dork.exe"]
        print("✔ spawn(argv={})".format(argv))
        pid = self._device.spawn(argv)
        self._instrument(pid)

    def _stop_if_idle(self):
        if len(self._sessions) == 0:
            self._stop_requested.set()

    def _instrument(self, pid):
        print("✔ attach(pid={})".format(pid))
        session = self._device.attach(pid)
        session.on("detached", lambda reason: self._reactor.schedule(lambda: self._on_detached(pid, session, reason)))
        print("✔ enable_child_gating()")
        session.enable_child_gating()
        print("✔ create_script()")
        script = session.create_script("""'use strict';

var module = Process.findModuleByName('dork.exe');
DebugSymbol.load("D:/instrmcpp/dork/firda_example/dork.exe");
var mainFunc=DebugSymbol.getFunctionByName("main")
Interceptor.attach(mainFunc, {
  onEnter: function (args) {
    send(args[0]);
  }
});
//message: pid=73552, payload={'type': 'send', 'payload': '0x1'}

var funcAddrLs=DebugSymbol.findFunctionsMatching("*ZUser*");
for (let funcAddr of funcAddrLs) {
Interceptor.attach(funcAddr, {
  onEnter: function (args) {
    send(args[0]);
  }
});
}
/*
⚡ message: pid=13460, payload={'type': 'send', 'payload': '0x5155cff9b8'}
⚡ message: pid=13460, payload={'type': 'send', 'payload': '0x230ffcfb720'}
⚡ message: pid=13460, payload={'type': 'send', 'payload': '0x230ffcfb720'}
⚡ message: pid=13460, payload={'type': 'send', 'payload': '0x230ffcfb720'}
⚡ message: pid=13460, payload={'type': 'send', 'payload': '0x5155cff9b8'}
*/


""")
        script.on("message", lambda message, data: self._reactor.schedule(lambda: self._on_message(pid, message)))
        print("✔ load()")
        script.load()
        print("✔ resume(pid={})".format(pid))
        self._device.resume(pid)
        self._sessions.add(session)

    def _on_delivered(self, child):
        print("⚡ delivered: {}".format(child))
        self._instrument(child.pid)

    def _on_detached(self, pid, session, reason):
        print("⚡ detached: pid={}, reason='{}'".format(pid, reason))
        self._sessions.remove(session)
        self._reactor.schedule(self._stop_if_idle, delay=0.5)

    def _on_message(self, pid, message):
        print("⚡ message: pid={}, payload={}".format(pid, message ))


app = Application()
app.run()