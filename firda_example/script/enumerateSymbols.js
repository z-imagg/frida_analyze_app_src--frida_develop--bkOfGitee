//  https://frida.re/docs/javascript-api/#module
var module = Process.findModuleByName('dork.exe');
var symbols=module.enumerateSymbols();
send(symbols);