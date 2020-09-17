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

        //json読み込み
        var tango_data = JSON.parse($("#hello-data").text());
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
                $('.result-ans').show();
                SendJson(tango_data);
                return;
            }

            //隠す
            $('.wrong-ans').hide();
            $('.correct-ans').hide();
            cnt = Rewrite(tango_data,cnt);
        
    });
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
