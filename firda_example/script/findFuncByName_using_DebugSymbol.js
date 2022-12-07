// https://frida.re/docs/javascript-api/

DebugSymbol.load("D:/instrmcpp/dork/cmake-build-debug/dork.exe");
var mainFunc=DebugSymbol.getFunctionByName("main");
//send(mainFunc);
//{'type': 'send', 'payload': '0x7ff7401e15d0'}

var funcAddrLs=DebugSymbol.findFunctionsMatching("*ZUser*");
//send(fLs);
//{'type': 'send', 'payload': ['0x7ff7401e17a0', '0x7ff7401e1870', '0x7ff7401e1830']}

for (let funcAddr of funcAddrLs) {
    var funcK=DebugSymbol.fromAddress(funcAddr);
    send(funcK);
}
//{'type': 'send', 'payload': {'address': '0x7ff7401e17a0', 'name': "ZUser::`scalar deleting destructor'", 'moduleName': 'dork.exe', 'fileName': '', 'lineNumber': 0, 'column': 0}}
//{'type': 'send', 'payload': {'address': '0x7ff7401e1870', 'name': 'ZUser::~ZUser', 'moduleName': 'dork.exe', 'fileName': 'D:\\instrmcpp\\dork\\ZUser.cpp', 'lineNumber': 11, 'column': 0}}
//{'type': 'send', 'payload': {'address': '0x7ff7401e1830', 'name': 'ZUser::ZUser', 'moduleName': 'dork.exe', 'fileName': 'D:\\instrmcpp\\dork\\ZUser.cpp', 'lineNumber': 7, 'column': 0}}