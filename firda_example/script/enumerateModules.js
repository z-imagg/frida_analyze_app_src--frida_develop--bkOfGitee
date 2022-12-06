//  https://frida.re/docs/javascript-api/#process-enumeratemodules
var modules = Process.enumerateModules();
for (let module of modules) {
    send(module);
}