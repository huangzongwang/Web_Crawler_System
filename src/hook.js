function logInf(classs){
    Java.perform(function (){
        var Modifier = Java.use("java.lang.reflect.Modifier");
        var Field = Java.use("java.lang.reflect.Field");
        var modifiers = classs.getModifiers();
        classs.setAccessible(true);
        if (Modifier.isStatic(modifiers)) {
            // 静态字段
            var value = classs.get(null);
            console.log(classs + " =>"  + value)
        } else {
             console.log(classs)
        }
    })
 
 
}
function getAllsonClass(classs){
    console.log('\n')
    console.log("查询到子类  =>" + classs.getName())
    hookClass(String(classs.getName()))
}


var thisclass = null;
//"java.security.MessageDigest"
function hookClass(CLASS){
Java.perform(function(){
    var classStudent = Java.use(CLASS);
    var classs = classStudent.class;
 
    //获取所有内部类
    var innerClasses = classs.getDeclaredClasses();
    if(innerClasses.length > 0){
        innerClasses.forEach(getAllsonClass);
    }
    console.log("===========" + classs + "中的所有变量==============")

    //输出所有变量
    classs.getDeclaredFields().forEach(logInf)
    console.log("===========" + classs +  "的所有方法==============")
    //输出所有方法,并hook
    classs.getDeclaredMethods().forEach(function(method){
        console.log(method)
       var methodsName = method.getName();
       var overloads  = classStudent[methodsName].overloads;
       console.log(overloads.length)
       for (var i=0; i< overloads.length; i++){
            overloads[i].implementation = function () {

            console.log('\n')
            console.warn("进入" + classs.getName() + "类的" + methodsName + "方法")
            for(var j=0; j<arguments.length; j++){
                console.error("参数" + j + " => " + arguments[j])
            }
            if (arguments.length === 0) {
              console.log("该函数无参数");
            }
            var result = this[methodsName].apply(this,arguments)

            console.error("结果是 => " + result)
           
            console.log("==1=2=3===01==1=1=1=11=21=");
            return result;
            
            };
        }
    })
    console.log('\n')
})
}

// hookClass("com.tencent.mm.vfs.r6")
// hookClass("com.tencent.mm.sdk.platformtools.x")
// hookClass('com.tencent.mm.graphics.e')
// hookClass('com.tencent.mm.vfs.f4')
// 
Java.perform(function(){
// let x = Java.use("com.tencent.mm.sdk.platformtools.x");
// console.log(x)
// x["B"].implementation = function (options, bArr, str, uri, inputStream, z16, i16) {
//     console.log(`x.B is called: options=${options}, bArr=${bArr}, str=${str}, uri=${uri}, inputStream=${inputStream}, z16=${z16}, i16=${i16}`);
//     let result = this["B"](options, bArr, str, uri, inputStream, z16, i16);
//     console.log(`x.B result=${result}`);
//     return result;
// };
// let e = Java.use("com.tencent.mm.graphics.e");

// e["g"].implementation = function (inputStream, rect, options) {
//     console.log(`e.g is called: inputStream=${inputStream}, rect=${rect}, options1=${options}`);
//     var fields=options.class.getDeclaredFields()
//     for(var j=0; j<fields.length; j++){
//         fields[j].setAccessible(true)
//         console.log(fields[j].get(options)+"================="+fields[j]);
//     }
//     let result = this["g"](inputStream, rect, options);
//     console.log(`e.g result=${result}`);
//     return result;
// };

let h4 = Java.use("com.tencent.mm.vfs.v6");
h4["E"].implementation = function (str) {
    console.log(`h4.y is called: str=${str}`);
    let result = this["E"](str);
    console.log(`h4.y result=${result}`);
    return result;
};


// var fileOutputStream = Java.use('com.tencent.mm.vfs.f4').$new('/sdcard/e7810efb5bd76e2e3facc9b35653c12a.jpg');
// var options=Java.use("com.tencent.mm.graphics.MMBitmapFactoryImpl.Options").$new()
// console.log(options);
// var srgbColorSpace = ColorSpace.get(ColorSpace.Named.SRGB)
// options.inBitmap=null
// options.inDensity=0
// options.inDither=false
// options.inInputShareable=false
// options.inJustDecodeBounds=false
// options.inMutable=false
// options.inPreferQualityOverSpeed=false
// options.inPreferredColorSpace=srgbColorSpace
// options.inPreferredConfig=Bitmap.Config.ARGB_8888
// options.inPremultiplied=true
// options.inPurgeable=false
// options.inScaled=false
// options.inSampleSize=0
// options.inScreenDensity=0
// options.inTempStorage=null
// options.inTargetDensity=0
// options.mCancel=false
// options.outColorSpace=srgbColorSpace
// options.outConfig=Bitmap.Config.ARGB_8888
// options.outHeight=1920
// options.outMimeType="image/wxam"
// options.outWidth=1080
// console.log(options);
// var bitm=MMBitmapFactoryImpl.getInstance().nativeDecodeStream(fileOutputStream,null,options)
// console.log(bitm);

// MMBitmapFactoryImpl["nativeDecodeStream"].implementation = function (inputStream, rect, options) {
//     var fileOutputStream = Java.use('com.tencent.mm.vfs.f4').$new('/sdcard/e7810efb5bd76e2e3facc9b35653c12a.jpg');
//     let result = this["nativeDecodeStream"](fileOutputStream, rect, options);
//     console.log(result);
//     if (result!=null){

//         console.log("contents: =====> ",inputStream.read());
//         var fileOutputStream = Java.use('java.io.FileOutputStream').$new('/sdcard/output');
//         var len;
//         var buffer = this.getOrCreateStorageBuffer(options)
//         console.log(buffer);
//         // 不断读取inputStream中的数据，直到读完为止
//         while ((len = inputStream.read(buffer, 0, 1024)) != -1) {
//             fileOutputStream.write(buffer, 0, len);
//         }
//         fileOutputStream.close()
//         console.log(`MMBitmapFactoryImpl.nativeDecodeStream is called111: inputStream=${inputStream}, rect=${rect}, options=${options}`);
//         var fields=options.class.getDeclaredFields()
//         for(var j=0; j<fields.length; j++){
//             fields[j].setAccessible(true)
//             console.log(fields[j].get(options)+"=======11====1======"+fields[j]+"");
//         }
//         console.log(`MMBitmapFactoryImpl.nativeDecodeStream result=${result}\n\n\n\n\n\n\n\n`);

//     }
//     return result;
// };
// MMBitmapFactoryImpl["nativeDecodeFileDescriptor"].implementation = function (fileDescriptor, bArr, rect, options) {
//     console.log(`MMBitmapFactoryImpl.nativeDecodeFileDescriptor is called: fileDescriptor=${fileDescriptor}, bArr=${bArr}, rect=${rect}, options=${options}`);
//     let result = this["nativeDecodeFileDescriptor"](fileDescriptor, bArr, rect, options);
//     console.log(`MMBitmapFactoryImpl.nativeDecodeFileDescriptor result=${result}`);
//     return result;
// };

})
