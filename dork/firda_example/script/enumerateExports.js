//  https://frida.re/docs/javascript-api/#module
var module = Process.findModuleByName('dork.exe');
var imports=module.enumerateExports();
send(imports);