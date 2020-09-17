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

    //jsonをgetする(ダミーデータ)
    const tango_data  = {
        "data" : 
        [
            {
                "word": "fact",
                "mean": ["真実","顔","太る","速い"],
                "flag": ["correct","wrong","wrong","wrong"]
            },
            {
                "word": "red",
                "mean": ["黄","青","赤","緑"],
                "flag": ["wrong","wrong","correct","wrong"]
            },
            {
                "word": "blue",
                "mean": ["白","青","黒","紫"],
                "flag": ["wrong","correct","wrong","wrong"]
        }]};

    //カウント用変数
    var cnt = 0;

    function Rewrite(tango_data,cnt){
        //htmlを受け取ったデータで書き換える
        //単語名
        $(".question-name").text(`${tango_data.data[cnt].word}`);

        ////
        console.log(cnt);
        console.log(typeof(word_name));
        console.log(`${Object.keys(tango_data)[cnt]}`);
        console.log(`${tango_data.data[cnt].word}`);

        
        //mean名
        for (let i = 0; i < 4; i++) {
            $(`.sbm-ans-btn${i}`).text(`${tango_data.data[cnt].mean[i]}`); 
        }
        
        //flag名
        for (let i = 0; i < 4; i++) {
            $(`.sbm-ans-btn${i}`).attr("id",`${tango_data.data[cnt].flag[i]}`); 
        }

        //解答をクリックすると正誤と答えが現れる
        $(".sbm-ans").click(function ()  {
            if ($(this).attr('id')==='correct'){
                $('.correct-ans').show();
            }
            else{
                $('.wrong-ans').show();
            }
        });
        
        //インクリメント
        return cnt + 1;
    };

    window.onload = () => {
        console.log('コンソール画面に文字を表示');

        //json読み込み
        var docm = document.getElementById('hello-data').textContent;
        console.log(docm);
        var tango_data = JSON.parse(docm);
        console.log(tango_data);

        cnt = Rewrite(tango_data,cnt);
        
    }

    //次へボタンで次の問題へ
    $(".toNext").click(function ()  {
        //終了条件
        if (cnt === 3){
            $('.wrong-ans').hide();
            $('.correct-ans').hide();
            $('.result-ans').show();
            return;
        }

        //隠す
        $('.wrong-ans').hide();
        $('.correct-ans').hide();
        cnt = Rewrite(tango_data,cnt);
        
        
    });


    //解答をクリックすると正誤と答えが現れる
    $(".sbm-ans").click(function ()  {
        if ($(this).attr('id')==='correct'){
            $('.wrong-ans').hide();
            $('.correct-ans').show();
        }
        else{
            $('.correct-ans').hide();
            $('.wrong-ans').show();
        }
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
