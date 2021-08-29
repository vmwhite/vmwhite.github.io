var width = $(window).width(); 
window.onscroll = function(){
if ((width >= 1000)){
    if(document.body.scrollTop > 80 || document.documentElement.scrollTop > 80) {
        if (document.body.classList.contains("dark-mode")) {
            $("#header").css("background","rgb(13, 0, 3)");
            $("#header").css("color","#fff");
            $("#header").css("box-shadow","0px 0px 20px rgba(0,0,0,0.09)");
            $("#header").css("padding","4vh 4vw");
            $("#logo").css("color", "rgb(255,44,90)");
            $("#navigation a").hover(function(){
                $(this).css("border-bottom","2px solid rgb(255, 44, 90)");
            },function(){
                $(this).css("border-bottom","2px solid transparent");
            });
        } else {
            $("#header").css("background","#fff");
            $("#header").css("color","#000");
            $("#header").css("box-shadow","0px 0px 20px rgba(0,0,0,0.09)");
            $("#header").css("padding","4vh 4vw");
            $("#logo").css("color", "rgb(255,44,90)"); 
            $("#navigation a").hover(function(){
                $(this).css("border-bottom","2px solid rgb(255, 44, 90)");
            },function(){
                $(this).css("border-bottom","2px solid transparent");
            });
        }  
    }else{
        $("#header").css("background","transparent");
        $("#header").css("color","#fff");
        $("#header").css("box-shadow","0px 0px 0px rgba(0,0,0,0)");
        $("#header").css("padding","6vh 4vw");
        $("#logo").css("color", "transparent");
        $("#navigation a").hover(function(){
            $(this).css("border-bottom","2px solid #fff");
        },function(){
            $(this).css("border-bottom","2px solid transparent");
        });
    }
}
}

function magnify(imglink){
    $("#img_here").css("background",`url('${imglink}') center center`);
    $("#magnify").css("display","flex");
    $("#magnify").addClass("animated fadeIn");
    setTimeout(function(){
        $("#magnify").removeClass("animated fadeIn");
    },800);
}

function closemagnify(){
    $("#magnify").addClass("animated fadeOut");
    setTimeout(function(){
        $("#magnify").css("display","none");
        $("#magnify").removeClass("animated fadeOut");
        $("#img_here").css("background",`url('') center center`);
    },800);
}

setTimeout(function(){
    $("#loading").addClass("animated fadeOut");
    setTimeout(function(){
      $("#loading").removeClass("animated fadeOut");
      $("#loading").css("display","none");
    },800);
},1650);

$(document).ready(function(){
    $("a").on('click', function(event) {
      if (this.hash !== "") {
        event.preventDefault();
        var hash = this.hash;
        $('body,html').animate({
        scrollTop: $(hash).offset().top
        }, 1800, function(){
        window.location.hash = hash;
       });
       } 
      });
  });
  
  function themeToggle() {
    var body = document.body
    var newClass = body.className == 'dark-mode' ? 'light-mode' : 'dark-mode'
    body.className = newClass
    var endDate = new Date();
    endDate.setFullYear(endDate.getFullYear() + 10);
        
    if ((width >= 1000)){
        if(document.body.scrollTop > 80 || document.documentElement.scrollTop > 80) {
            if (document.body.classList.contains("dark-mode")) {
                $("#header").css("background","rgb(13, 0, 3)");
                $("#header").css("color","#fff");
                $("#header").css("box-shadow","0px 0px 20px rgba(0,0,0,0.09)");
                $("#header").css("padding","4vh 4vw");
                $("#navigation a").hover(function(){
                    $(this).css("border-bottom","2px solid rgb(255, 44, 90)");
                },function(){
                    $(this).css("border-bottom","2px solid transparent");
                });
            } else {
                $("#header").css("background","#fff");
                $("#header").css("color","#000");
                $("#header").css("box-shadow","0px 0px 20px rgba(0,0,0,0.09)");
                $("#header").css("padding","4vh 4vw");
                // $("#navigation a").css("color","#fff"); attempt to make header labels same at the rest
                $("#navigation a").hover(function(){
                    $(this).css("border-bottom","2px solid rgb(255, 44, 90)");
                },function(){
                    $(this).css("border-bottom","2px solid transparent");
                });
            }
        }else{
            $("#header").css("background","transparent");
            $("#header").css("color","#fff");
            $("#header").css("box-shadow","0px 0px 0px rgba(0,0,0,0)");
            $("#header").css("padding","6vh 4vw");
            $("#navigation a").hover(function(){
                $(this).css("border-bottom","2px solid #fff");
            },function(){
                $(this).css("border-bottom","2px solid transparent");
            });
        }
    }

    document.cookie = 'theme=' + (newClass == 'light-mode' ? 'light' : 'dark') +
    '; Expires=' + endDate + ';'
    console.log('Cookies are now: ' + document.cookie)
  }

  function isDarkThemeSelected() {
    return document.cookie.match(/theme=dark/i) != null
  }

  function setThemeFromCookie() {
    document.body.className = isDarkThemeSelected() ? 'dark-mode' : 'light-mode'
  }

