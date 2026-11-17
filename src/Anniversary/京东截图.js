// 
function runscript() {
    try {
        toast('截图脚本启动')
        sleep(200)
        launch("com.jd.jdlogistic");
        toast('打开app')
        sleep(3000);
        if (!requestScreenCapture()) {
            toast("请求截图失败");
            exit();
        }
        sleep(5000)
        toast('查找列表')
        var isrun = true
        var index = 0
        do {
            var ydh = textStartsWith('运单号：').find()
            if (ydh.size() > 0) {
                if (index < ydh.size()) {
                    var result = index_run(index, ydh)
                    if (result) {
                        index = index + 1
                    }
                } else {
                    swipe(device.width * 0.5, 0.6 * device.height, 0.5 * device.width, 0.5 * device.height, 100)
                    sleep(1000)
                    toast('下一页数据')
                    index = 0
                }
            } else {
                captureScreen("/sdcard/order/screencapture1111.png");
                /* OCR 识别并获取结果, 结果为字符串数组. */
                let results = ocr("/sdcard/order/screencapture1111.png");
                var isSuccess = false
                if (results.length > 0) {
                    for (var i = 0; i < results.length; i++) {
                        var result_index = results[i]
                        console.log(result_index);
                        if (result_index != undefined) {
                            if (result_index.indexOf("物品信息") != -1) {
                                isSuccess = true
                            }
                            if (result_index.indexOf("运单号") != -1) {
                                isSuccess = true
                            }
                            if (result_index.indexOf("平台单号") != -1) {
                                isSuccess = true
                            }
                        }
                    }
                    if (isSuccess) {
                        if(textStartsWith("我寄").exists()){
                        }else{
                            back()
                        }
                        sleep(1500)
                        if(textStartsWith("我寄").exists()){
                        }else{
                            back()
                            sleep(300)
                        }
                    }
                    sleep(300)
                }
            }
        } while (isrun);
    } catch (error) {
        console.log(error)
        toast(error)
    }
}
function index_run(index, ydh) {
    var order = ydh.get(index)
    var result_run = false
    if (order != null) {
        order_id = ""
        if (files.exists("/sdcard/order_recorecord.txt")) {
            order_id = files.read("/sdcard/order_recorecord.txt")
        }
        desc = order.text()
        if (order_id.indexOf(desc) == -1) {
            order_id = order_id + "\n" + desc
            var right = order.bounds().right+100
            var bottom = order.bounds().bottom+100
            // var parent = order.parent().parent().parent().parent()
            if (bottom < 1900 ) {
                click(right,bottom)
                sleep(800)
                text('电子存根').findOne(3000).click()
                sleep(1000)
                var s=textContains('****').find()
                for (var i = 0; i < s.length; i++) {
                    right=s.get(i).bounds().right
                    bottom=s.get(i).bounds().bottom
                    click(right+100,bottom)
                    sleep(100)
                }
                sleep(800)
                captureScreen("/sdcard/order/screencapture" + desc.substring(7, desc.length - 1) + ".png");
                sleep(300)
                /* OCR 识别并获取结果, 结果为字符串数组. */
                let results = ocr("/sdcard/order/screencapture" + desc.substring(7, desc.length - 1) + ".png");
                var isSuccess = false
                if (results.length > 0) {
                    for (var i = 0; i < results.length; i++) {
                        var result_index = results[i]
                        console.log(result_index);
                        if (result_index != undefined) {
                            if (result_index.indexOf("物品信息") != -1) {
                                isSuccess = true
                            }
                            if (result_index.indexOf("运单号") != -1) {
                                isSuccess = true
                            }
                            if (result_index.indexOf("平台单号") != -1) {
                                isSuccess = true
                            }
                        }
                    }
                }
                if (isSuccess) {
                    files.append("/sdcard/order_recorecord.txt", desc + "\n");
                    toast('截图成功，返回列表')
                    result_run = true
                } else {
                    result_run = false
                    files.remove("/sdcard/order/screencapture" + desc.substring(7, desc.length - 1) + ".png")
                    toast('截图失败')
                }
                if(textStartsWith("我寄").exists()){
                }else{
                    back()
                }
                sleep(1500)
                if(textStartsWith("我寄").exists()){
                }else{
                    back()
                    sleep(300)
                }
                
                // } else {
                //     result_run = false
                //     toast('点击失败,请联系技术人员协助')
                // }
            } else {
                result_run = false
            }
          
        } else {
            result_run = true
        }
    } else {
        result_run = false
    }
    return result_run
}
threads.start(function () {
    runscript()
});
threads.start(function () {
    while (true) {
        sleep(1200);
        if (text('暂不升级').exists()) {
            text('暂不升级').click();
        };
    };
});