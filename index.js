const mediaQuery = window.matchMedia('(min-width: 1000px)')
window.onscroll = function(){
if ((mediaQuery.matches)){
    if(document.body.scrollTop > 80 || document.documentElement.scrollTop > 80) {
        $("#logo").css("color", "rgb(255,44,90)"); 
        $("header").css("box-shadow","0% 0% 20% rgba(0,0,0)");
        if (document.body.classList.contains("dark-mode")) {
            $("header").css("background","rgb(13, 0, 3)");
            $("#navigation a").css("color","#fff");
        } else {
            $("#header").css("background","#fff");
            $("#navigation a").css("color","#000");
        }  
    }else{
        $("#logo").css("color", "transparent");
        $("header").css("background","transparent");
        $("header").css("box-shadow","0% 0% 0% rgba(0,0,0,0)");
        if (document.body.classList.contains("dark-mode")) {
            $("#navigation a").css("color","#fff");
        } else {
            $("#navigation a").css("color","#fff");
        }  
    }
}else{
    $("header").css("background","solid");
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

//   To change darkmode based on os/system dark mode presets
//   https://css-tricks.com/a-complete-guide-to-dark-mode-on-the-web/#aa-using-a-body-class
  function themeToggle() {
    var body = document.body
    var newClass = body.className == 'dark-mode' ? 'light-mode' : 'dark-mode'
    body.className = newClass
    var endDate = new Date();
    endDate.setFullYear(endDate.getFullYear() + 10);
    if ((mediaQuery.matches)){
        if(document.body.scrollTop > 80 || document.documentElement.scrollTop > 80) {
            $("#logo").css("color", "rgb(255,44,90)"); 
            $("header").css("box-shadow","0% 0% 20% rgba(0,0,0)");
            if (document.body.classList.contains("dark-mode")) {
                $("header").css("background","rgb(13, 0, 3)");
                $("#navigation a").css("color","#fff");
            } else {
                $("#header").css("background","#fff");
                $("#navigation a").css("color","#000");
            }  
        }else{
            $("#logo").css("color", "transparent");
            $("header").css("background","transparent");
            $("header").css("box-shadow","0% 0% 0% rgba(0,0,0,0)");
            if (document.body.classList.contains("dark-mode")) {
                $("#navigation a").css("color","#fff");
            } else {
                $("#navigation a").css("color","#fff");
            }  
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

