'use strict';

var module = Process.findModuleByName('dork.exe');
//猜测: DebugSymbol.load 依赖 .exe文件 的 同目录 的 同名 .pdb文件
DebugSymbol.load("D:/instrmcpp/dork/cmake-build-debug/dork.exe");
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