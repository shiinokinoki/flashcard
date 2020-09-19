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
    function SendResult(tango_data){
        var send_data = {"data": []};
        
        /*
        {"data": [
            {"id":"nan","result":"nan"},
            {"id":"nan","result":"nan"},
            {"id":"nan","result":"nan"},
        ]};
        */ 
        console.log(tango_data);
        console.log(tango_data.data.length);
        for (let i = 0; i < tango_data.data.length; i++) {
            send_data.data.push({"id":"nan","result":"nan"});
            console.log(send_data.data);
            send_data.data[i].id = tango_data.data[i].id;
            send_data.data[i].result = tango_data.data[i].result;   
        }
        
        console.log(send_data);
        JsonSender(tango_data,JSON.stringify(send_data));

    }

    //JSONdataを送信する
    function JsonSender(tango_data,JSONdata){
        console.log(tango_data);
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
        var cur_url = URLJoin(root_url, "wordbook",`${tango_data.url}`);
        console.log(`tango_data =`);
        console.log(tango_data);
        console.log(`tango_data.url = ${tango_data.url}`)
        // 4 POST先と送信したい値の設定 TODO urlの名前
        var post_url = cur_url // +"/";

        // 5 csrfを設定する関数を実行して、POSTを実行
        csrfSetting();
        $.post(post_url, JSONdata);
        console.log(`送信完了 JSONdata = ${JSONdata}`);
        console.log(`url = ${cur_url}`);
    };

    //main関数
    window.onload = () => {
        console.log('コンソール画面に文字を表示');

        //tango_dataの宣言
        var tango_data;

        //ダミーデータ
        tango_data = {
            "pagename": "question",
            "url" : "learning/result/",
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
        
        //question画面でのjs関数
        function jsQuestion(){
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
                    //結果送信
                    $("#send-result").click(function(){
                        SendResult(tango_data);
                    });
                    return;
                }

                //隠す
                $('.wrong-ans').hide();
                $('.correct-ans').hide();
                cnt = Rewrite(tango_data,cnt);
            
            });
        };

        //register画面でのjs関数
        function jsRegister(){

            //DOMの追加
            /*
            <div class="container">
                <div class="row">
                    <div class="col-md-6 mb-3 mb-md-0">
                        <div class="dropdown">
                            <button type="button" id="dropdown1" class="btn btn-secondary dropdown-toggle bg-black"
                                data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                fact
                            </button>
                            <ul class="dropdown-menu" aria-labelledby="dropdown1">
                                <div class="jAppend ${i}" ></div>
                            </ul>
                        </div>
                    </div>
                    <div class="col-md-6 mb-3 mb-md-0">
                        <div class="card py-3 h-100 bg-dark text-white">
                            <p class="card-text text-danger" id='card${i}'>未入力</p>
                        </div>
                    </div>
                </div>
            </div>
            <!-- 改行-->
            <hr class="my-4" />
            */

            

            var i = 0;
            var j = 0;
            for (let i = 0; i < tango_data.data.length; i++) {
                ////
                console.log(`${i}回目！！！！！`)
                console.log(tango_data.data[i]);

                //DOM追加
                $('.iAppend').append(`<div class="container"><div class="row"><div class="col-md-6 mb-3 mb-md-0"><div class="dropdown"><button type="button" id="dropdown${i}" class="btn btn-secondary dropdown-toggle bg-black"data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">fact</button><ul class="dropdown-menu" aria-labelledby="dropdown1"><div class="jAppend${i}"></div></ul></div></div><div class="col-md-6 mb-3 mb-md-0"><div class="card py-3 h-100 bg-dark text-white"><p class="card-text text-danger" id='card${i}'>未入力</p></div></div></div></div><!-- 改行--><hr class="my-4" />`);       
                //名前追加
                $(`#dropdown${i}`).text(`${tango_data.data[i].word}`);
                console.log(tango_data.data[i].word);
                for (let j = 0; j < tango_data.data[i].mean.length; j++) {
                    //DOM追加
                    $(`.jAppend${i}`).append(`<li class="dropdown-item i${i}" id="j${j}" value="v${j}"></li>`);
                    //選択肢追加
                    console.log(`i,j = ${i}#${j}`);
                    console.log($(`.i${i}` + `#j${j}`).text());
                    $(`.i${i}` + `#j${j}`).text(`${tango_data.data[i].mean[j]}`);
                    console.log(tango_data.data[i].mean[j]);
                }
                
            }
            
            


            return;
        };

        if (tango_data.pagename === "question"){
            jsQuestion();
        }
        else if (tango_data.pagename === "register_list"){
            console.log('register_list');
            jsRegister();

            //ドロップダウンの操作 TODO 色の変化
            $('.dropdown-item').click(function () {
                //通常16文字 ex)dropdown-item i6
                var eleLeng = $(this).attr('class').length;
                var eleNum;
                if (eleLeng == 16){
                    eleNum = 1
                } else if (eleLeng == 17){
                    eleNum = 2
                } else if (eleLeng == 18){
                    eleNum = 3
                }

                $(`#card${$(this).attr('class').slice(eleLeng - eleNum)}`).text($(this).text());
            });

            //カードの記録を送信
            var send_data = {"data": []};
            $("#send-result").click(function(){
                for (let i = 0; i < tango_data.data.length; i++) {
                    var mean = $(`#card${i}`).text();
                    console.log(`mean = ${mean}`);

                    /*
                    {"data": [
                        {"id":"nan","mean":"nan"},
                        {"id":"nan","mean":"nan"},
                        {"id":"nan","mean":"nan"},
                    ]};
                    */ 
                    send_data.data.push({"word":tango_data.data[tango_data.data[i].id].word,"mean":mean});
                    
                }
                console.log(send_data);
                JsonSender(tango_data,JSON.stringify(send_data));

            });
        }
        
    }


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