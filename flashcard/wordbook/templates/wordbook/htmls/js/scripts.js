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
        'fact' : 
        [{
            'mean': ['意味1','意味2','意味3','意味4'],
            'flag': [true,false,false,false]
        }],
        'red' : 
        [{
            'mean': ['意味1','意味2','意味3','意味4'],
            'flag': [false,false,true,false]
        }],
        'blue' :
        [{
            'mean': ['意味1','意味2','意味3','意味4'],
            'flag': [false,true,false,false]
        }],
    }

    //カウント用変数
    let cnt = 0;

    function Rewrite(tango_data,cnt){
        //htmlを受け取ったデータで書き換える
        //単語名
        let word_name = Object.keys(tango_data)[0];
        $(".question-name").text(word_name);

        ////
        console.log(cnt);
        console.log(typeof(word_name));
        console.log(`${Object.keys(tango_data)[0]}`);
        console.log(`${tango_data.fact[0].mean[0]}`);
        console.log(`${tango_data[1]}`);
        console.log(`${tango_data.word_name[0].mean[0]}`);
        
        //mean名
        $(".sbm-ans-btn0").text(`${tango_data[word_name].mean[0]}`);
        $(".sbm-ans-btn1").text(`${tango_data[word_name].mean[1]}`);
        $(".sbm-ans-btn2").text(`${tango_data[word_name].mean[2]}`);
        $(".sbm-ans-btn3").text(`${tango_data[word_name].mean[3]}`);
        //flag名
        $(".sbm-ans-btn0").attr("id",`${tango_data[word_name].flag[0]}`);
        $(".sbm-ans-btn1").attr("id",`${tango_data[word_name].flag[1]}`);
        $(".sbm-ans-btn2").attr("id",`${tango_data[word_name].flag[2]}`);
        $(".sbm-ans-btn3").attr("id",`${tango_data[word_name].flag[3]}`);

        //実験
        $(".sbm-ans-btn0").text(`aiueo`);

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
        cnt = cnt + 1;
    };

    window.onload = () => {
        console.log('コンソール画面に文字を表示');
        Rewrite(tango_data,cnt);
    }

    //次へボタンで次の問題へ
    $(".toNext").click(function ()  {
        Rewrite(tango_data,cnt);
        if (cnt == 3){
            alert('おわりです');
        }
    });


    //解答をクリックすると正誤と答えが現れる
    $(".sbm-ans").click(function ()  {
        if ($(this).attr('id')==='correct'){
            $('.correct-ans').show();
        }
        else{
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
