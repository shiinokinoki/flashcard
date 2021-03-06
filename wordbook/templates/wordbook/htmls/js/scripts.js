/*!
    * Start Bootstrap - Grayscale v6.0.2 (https://startbootstrap.com/themes/grayscale)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-grayscale/blob/master/LICENSE)
    */
   (function ($) {
    "use strict"; // Start of use strict

    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
        if (
            location.pathname.replace(/^\//, "") ==
                this.pathname.replace(/^\//, "") &&
            location.hostname == this.hostname
        ) {
            var target = $(this.hash);
            target = target.length
                ? target
                : $("[name=" + this.hash.slice(1) + "]");
            if (target.length) {
                $("html, body").animate(
                    {
                        scrollTop: target.offset().top - 70,
                    },
                    1000,
                    "easeInOutExpo"
                );
                return false;
            }
        }
    });

    // Closes responsive menu when a scroll trigger link is clicked
    $(".js-scroll-trigger").click(function () {
        $(".navbar-collapse").collapse("hide");
    });
    
    
    // Activate scrollspy to add active class to navbar items on scroll
    //スクロールスパイはメニュー(ナビゲーションバー、またはリストグループ)に応じて本文をスクロールします。
    //また、本文のスクロールを監視し、スクロールに応じてメニューの該当アイテムをアクティブにします。
    $("body").scrollspy({
        target: "#mainNav",
        offset: 100,
    });


    ///////////////////
    //question用
    ///////////////////


    //カウント用変数
    var cnt = 0;

    //問題を書き換える関数
    function Rewrite(tango_data,cnt){
        //htmlを受け取ったデータで書き換える

        ////
        console.log(`cnt = ${cnt}`);
        console.log(`${tango_data.data[cnt].word}`);
        //問題番号を変更
        $("#question-num").text(`${cnt+1}問目`);

        //単語名
        $(".question-name").text(`${tango_data.data[cnt].word}`);

        
        //mean名
        for (let i = 0; i < 4; i++) {
            $(`.sbm-ans-btn${i}`).text(`${tango_data.data[cnt].mean[i]}`); 
        }
        
        //flag名
        for (let i = 0; i < 4; i++) {
            $(`.sbm-ans-btn${i}`).attr("id",`${tango_data.data[cnt].flag[i]}`); 
        }
        
        //インクリメント
        return cnt + 1;
    };

    //リザルト画面表示
    function Result(tango_data){
        $('.ans-page').hide();
        $('.result-page').show();

        //総合得点
        var scorecnt = 0
        var maxscore = 0

        //単語の表示
        for (let i = 0; i < tango_data.data.length; i++) {
            $(`.words${i}`).text(`${tango_data.data[i].word}`);
            if (tango_data.data[i].result == "wrong"){
                $(`.Icon${i}`).removeClass("fas fa-check-square text-primary mb-2"); 
                $(`.Icon${i}`).addClass("fas fa-times-circle text-danger mb-2"); 
            }
            else{
                scorecnt = scorecnt + 1;
            };

            maxscore = maxscore + 1;
        }

        //結果表示
        $("#score1").text(scorecnt);
        $("#score2").text(`/${maxscore}`);

        //詳しく見るなら...
        $("#detail").click(function(){
            $("#result").toggle();
        });
        
        

        //TODO 自在にhtmlの数をjsで足す
        
    };

    //問題データを送信する
    function SendJson(tango_data){
        var send_data = {"data": []};
        
        console.log(tango_data);
        console.log(tango_data.data.length);
        for (let i = 0; i < tango_data.data.length; i++) {
            send_data.data.push({"id":"nan","result":"nan"});
            console.log(send_data.data);
            send_data.data[i].id = tango_data.data[i].id;
            send_data.data[i].result = tango_data.data[i].result;   
        }
        
        console.log(send_data);
    }

    
    window.onload = () => {
        console.log('コンソール画面に文字を表示');

        //tango_dataの宣言
        var tango_data;

        //ダミーデータ
        tango_data = {
            "ver": "question",
            "data": 
            [
                {
                    "id": "0001",
                    "word": "fact",
                    "mean": ["真実","顔","太る","速い"],
                    "flag": ["correct","wrong","wrong","wrong"],
                    "result": "nan"
                },
                {
                    "id": "0002",
                    "word": "red",
                    "mean": ["黄","青","赤","緑"],
                    "flag": ["wrong","wrong","correct","wrong"],
                    "result": "nan"
                },
                {
                    "id": "0003",
                    "word": "blue",
                    "mean": ["白","青","黒","紫"],
                    "flag": ["wrong","correct","wrong","wrong"],
                    "result": "nan"
        }]};
        //json読み込み
        tango_data = JSON.parse($("#hello-data").text());
        console.log(tango_data);
        

        cnt = Rewrite(tango_data,cnt);

        //解答をクリックすると正誤と答えが現れる
        $(".sbm-ans").click(function()  {
            console.log(tango_data);
            console.log((parseFloat($("#question-num").text()[0])));
            if ($(this).attr('id')=='correct'){
                $('.correct-ans').show();
                tango_data.data[parseFloat($("#question-num").text()[0])-1].result = 'correct';
                console.log(tango_data.data[parseFloat($("#question-num").text()[0])-1].result);
            }
            else{
                $('.wrong-ans').show();
                tango_data.data[parseFloat($("#question-num").text()[0])-1].result = 'wrong';
                console.log(tango_data.data[parseFloat($("#question-num").text()[0])-1].result);
            }
        });
        
        //次へボタンで次の問題へ
        $(".toNext").click(function ()  {
            //終了条件
            if (cnt === 3){
                $('.wrong-ans').hide();
                $('.correct-ans').hide();

                //リザルトを表示する
                Result(tango_data);
                $("#back-home").click(function(){
                    SendJson(tango_data);
                });
                return;
            }

            //隠す
            $('.wrong-ans').hide();
            $('.correct-ans').hide();
            cnt = Rewrite(tango_data,cnt);
        
    });
    }



    //json 送信
    function JsonSender(JSONdata){
        // 2 csrfを取得、設定する関数
        function getCookie(key) {
            var cookies = document.cookie.split(';');
            for (var _i = 0, cookies_1 = cookies; _i < cookies_1.length; _i++) {
                var cookie = cookies_1[_i];
                var cookiesArray = cookie.split('=');
                if (cookiesArray[0].trim() == key.trim()) {
                    return cookiesArray[1]; // (key[0],value[1])
                }
            }
            return '';
        }
        function csrfSetting() {
            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    }
                }
            });
        }

        // 3 POST以外は受け付けないようにする関数
        function csrfSafeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        const URLJoin = (...args) =>
        args
            .join('/')
            .replace(/[\/]+/g, '/')
            .replace(/^(.+):\//, '$1://')
            .replace(/^file:/, 'file:/')
            .replace(/\/(\?|&|#[^!])/g, '$1')
            .replace(/\?/g, '&')
            .replace('&', '?');
        var protoc = location.protocol;
        var url_host = location.host ;
        var root_url = protoc + "//" +url_host
        var cur_url = URLJoin(root_url, "wordbook","takepic","detimg");
        // 4 POST先と送信したい値の設定
        var post_url = cur_url+"/";
        var data = {
            'image': 'Hello',
        };

        // 5 csrfを設定する関数を実行して、POSTを実行
        csrfSetting();
        $.post(post_url, data);
    };

    //#send-jsonで送信できるようにする
    $("#send-json").click(function(){
        JsonSender(JsonSender(JSONdata));
    });


    // Collapse Navbar
    var navbarCollapse = function () {
        if ($("#mainNav").offset().top > 100) {
            $("#mainNav").addClass("navbar-shrink");
        } else {
            $("#mainNav").removeClass("navbar-shrink");
        }
    };
    // Collapse now if page is not at top
    navbarCollapse();
    // Collapse the navbar when page is scrolled
    $(window).scroll(navbarCollapse);
})(jQuery); // End of use strict