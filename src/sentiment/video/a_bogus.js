
window=watch(global,"window")

print={
    flag:!false,
    log:function(){
        if(this.flag){
            // console.log(...arguments)
        }
    }
}



function watch(proxyObjs,name) {
    var handler = {
        get: function (target, property, receiver) {
            // debugger

            // if(property ==="XMLHttpRequest" ||String(target)==="global" ||target[property] ==="undefined") debugger
            if(typeof target[property]==="function"){
                // if(property ==="fetch" ||property ==="Request"||property ==="XMLHttpRequest") return `function ${property}() { [native code] }`
                // if(property ==="fetch" ||property ==="Request"||property ==="XMLHttpRequest") debugger
                print.log("对象==>",name, "\t获取属性(get)：", property,  "\t值类型：function  ==>", typeof target[property]);
            }else{
                // if (property ==="_$e5"){debugger}
                print.log("对象==>",name, "\t获取属性(get)：", property, "\t值类型：", typeof target[property], "\t值：",target[property]);


            }

        return target[property];
        },
        set: function (target, property, value) {
            // debugger
            // print.log("对象==>",name, "\t设置属性(set)：", property, "\t属性值：", value, "\t属性值类型：", typeof value);
             print.log("对象==>",name, "\t设置属性(set)：", property, "\t属性值类型：", typeof value,"\t属性值：", value);
            //  if (property==="___TS___"){debugger}
            return Reflect.set(...arguments);
        },

    };
    return new Proxy(proxyObjs, handler);
}






function obj_toString(obj,name){
    Object.defineProperty(obj,Symbol.toStringTag,{
        value:name,
        configurable: true,
        writable: true,

    })
}
;
(() => {
    'use strict';
    // 取原型链上的toString
    const $toString = Function.toString;
    // 取方法名 reload
    const myFunction_toString_symbol = Symbol('('.concat('', ')_', (Math.random() + '').toString(36)));
    const myToString = function () {
        return typeof this == 'function' && this[myFunction_toString_symbol] || $toString.call(this);
    };

    function set_native(func, key, value) {
        Object.defineProperty(func, key, {
            "enumerable": false,  // 不可枚举
            "configurable": true, // 可配置
            "writable": true, // 可写
            "value": value
        })
    }

    delete Function.prototype['toString'];// 删除原型链上的toString
    set_native(Function.prototype, "toString", myToString); // 自定义一个getter方法，其实就是一个hook
    //套个娃，保护一下我们定义的toString，避免js对toString再次toString，如：location.reload.toString.toString() 否则就暴露了
    set_native(Function.prototype.toString, myFunction_toString_symbol, "function toString() { [native code] }");
    global.safefunction = (func) => {
        set_native(func, myFunction_toString_symbol, `function ${myFunction_toString_symbol,func.name || ''}() { [native code] }`);
    }; //导出函数到globalThis，更改原型上的toSting为自己的toString。这个方法相当于过掉func的toString检测点
}).call(global);





top = self = parent = window;

window.setInterval = function(){};window.safefunction(window.setInterval);

window.setTimeout = function(){};window.safefunction(window.setTimeout);

window.requestAnimationFrame = function(){};window.safefunction(window.requestAnimationFrame);

window,addEventListener = function(){};window.safefunction(window.addEventListener);

window._sdkGlueVersionMap = {sdkGlueVersion: '1.0.0.64-fix.01', bdmsVersion: '1.0.1.19-fix.01', captchaVersion: '4.0.10'}

window.fetch = function(){};window.safefunction(window.fetch);

window.EventSource = function() {};window.safefunction(window.EventSource);

window.OfflineAudioContext = function(){};window.safefunction(window.OfflineAudioContext);

window.CanvasRenderingContext2D = function(){};window.safefunction(window.CanvasRenderingContext2D);

window.onwheelx = {_Ax: '0X21'}






window.indexedDB = {}

window.innerWidth = 1812

window.innerHeight = 664

window.outerWidth = 1812

window.outerHeight = 974

window.screenX = 0

window.screenY = 0

window.pageYOffset = 0

window.pageXOffset = 0





/* document 对象 */

document = {

    all: {},

    createElement: function(tag){

        if(tag === 'span') return span;

        if(tag === 'canvas') return canvas;


        return {};

    },

    documentElement: {},

    createEvent: function(){

    },

    addEventListener: function(){

    },

};

window.safefunction(document.createElement);

window.safefunction(document.createEvent);

window.safefunction(document.addEventListener);


obj_toString(document,'HTMLDocument')

/* localStorage 对象 */

localStorage = {

    getItem: function(){},

};

window.safefunction(localStorage.getItem);


obj_toString(localStorage,'LocalStorage')

/* sessionStorage 对象 */

sessionStorage = {}


obj_toString(sessionStorage,'SessionStorage')

/* location 对象 */

location = {
    "ancestorOrigins": {},
    "href": "https://www.douyin.com/jingxuan?modal_id=7537260177221848366",
    "origin": "https://www.douyin.com",
    "protocol": "https:",
    "host": "www.douyin.com",
    "hostname": "www.douyin.com",
    "port": "",
    "pathname": "/jingxuan",
    "search": "?modal_id=7537260177221848366",
    "hash": ""
}



obj_toString(location,"Location")

/* navigator */

navigator = {
    userAgent:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    storage:{},
    platform:'Win32'
}
obj_toString(navigator,"Navigator")




/* history 对象 */

history = {}

obj_toString(history,'History')




/* screen 对象 */


screen = {

    availHeight:974,

    availLeft: 0,

    availTop: 0,

    availWidth: 1812,

    colorDepth: 24,

    height: 1019,

    isExtended: false,
    pixelDepth: 24,
    width: 1812,
    onchange: null,

    orientation: {

    angle: 0,

    type: 'landscape-primary',

    onchange: null

    }

}



obj_toString(screen,'Screen')

/* XMLHTTPREQUEST 对象 */

XMLHttpRequest = function XMLHttpRequest(){};window.safefunction(XMLHttpRequest);

XMLHttpRequest.prototype.send = function send(){};window.safefunction(XMLHttpRequest.prototype.send);

XMLHttpRequest.prototype.open = function open(){};window.safefunction(XMLHttpRequest.prototype.open);



/* span 对象 */

span = {

    classList: {},

}



/* canvas 对象 */

canvas = {

    getContext: function(){},

}

window.safefunction(canvas.getContext);



document=watch(document,"document")
locaion=watch({},"locaion")

navigator=watch(navigator,"navigator")
history=watch(history,"history")
screen=watch(screen,"screen")


localStorage=watch(localStorage,"localStorage")
sessionStorage=watch(sessionStorage,"sessionStorage")
span=watch(span,"span")
canvas=watch(canvas,"canvas")


require("./bdms")

//初始化
t={
    "aid": 6383,
    "pageId": 6241,
    "paths": [
        "^/webcast/",
        "^/aweme/v1/",
        "^/aweme/v2/",
        "/douplus/",
        "/v1/message/send",
        "^/live/",
        "^/captcha/",
        "^/ecom/"
    ],
    "boe": false,
    "ddrt": 8.5,
    "ic": 8.5
}

window.bdms.init(t);

function get_abogus(url,uifid){

    xhr = new XMLHttpRequest;

    xhr.bdmsInvokeList = [

        {"args": ["GET", url, true], func: function(){}},

        {"args": ["Accept","application/json, text/plain, */*"], func: function(){}},

        {"args": ["uifid", uifid], func: function(){}},


    ]
    xhr.invokeList=[
    {
        "name": "addEventListener",
        "args": [
            "load",
            null
        ]
    },
    {
        "name": "addEventListener",
        "args": [
            "error",
            null
        ]
    }
]

    xhr.send()
    console.log("window",window.a_bogus)
    return window.a_bogus

}

// get_abogus("https://www.douyin.com/aweme/v1/web/general/search/single/?device_platform=webapp&aid=6383&channel=channel_pc_web&search_channel=aweme_general&enable_history=1&keyword=%E8%B5%9B%E4%B9%90%E8%B5%9B%20%20%E9%AA%97%E5%B1%80&search_source=normal_search&query_correct_type=1&is_filter_search=0&from_group_id=&disable_rs=0&offset=10&count=10&need_filter_settings=0&list_type=multi&pc_search_top_1_params=%7B%22enable_ai_search_top_1%22%3A1%7D&search_id=20260205140011A4435104F57D8C41AB09&update_version_code=170400&pc_client_type=1&pc_libra_divert=Windows&support_h265=1&support_dash=1&cpu_core_num=20&version_code=190600&version_name=19.6.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=144.0.0.0&browser_online=true&engine_name=Blink&engine_version=144.0.0.0&os_name=Windows&os_version=10&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7594762525129000511&uifid=1b474bc7e0db9591e645dd8feb8c65aae4845018effd0c2743039a380ee64740bcd8a7cc6965c1b91fe4e044e3bac70399fb37071460ec7ee7081c8e2ce778579e81e2e12a3a15cb9d27e86d8e6c57a483c2afbcf7f564a9b9cfc5870676659d162c36de46f20446953513105d8fe3c7520a8f367d7d3b2e29ab943da3aa9c2cd35335cc0416549fe7e74c2788fd3c9039508fe4390fd02623826700aaa3e5dd","1b474bc7e0db9591e645dd8feb8c65aae4845018effd0c2743039a380ee64740bcd8a7cc6965c1b91fe4e044e3bac70399fb37071460ec7ee7081c8e2ce778579e81e2e12a3a15cb9d27e86d8e6c57a483c2afbcf7f564a9b9cfc5870676659d162c36de46f20446953513105d8fe3c7520a8f367d7d3b2e29ab943da3aa9c2cd35335cc0416549fe7e74c2788fd3c9039508fe4390fd02623826700aaa3e5dd")