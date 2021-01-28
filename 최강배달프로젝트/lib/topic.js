var db = require('./db');
var template = require('./template.js');
var topic = require('./topic.js');
var url = require('url');
var qs = require('querystring');
const { networkInterfaces } = require('os');
const { exception } = require('console');

exports.login = function(request,response){
  //var title = '로그인';
  var description = `로그인을 해주세요`;
  var list = `
  <form name="login" action="/userlogin" method="post">
      <p>
        <input type="text" name="id" placeholder="ID">
      </p>
      <p>
        <input type="password" name="pw" placeholder="PW">
        <input type="hidden" name="clearprocess" value="1">
      </p>
            <p>
              <input type="submit" value="로그인!">
            </p>
          </form>
        <h8><a href="/create">회원가입<br></a></h8>
 
  `;
  var control = `${control}`;
  var html = template.HTML(
    '로그인', 
    list,
    ``,
    `최강배달`
  );
  response.writeHead(200);
  response.end(html);
}

exports.create = function(request,response){
  var html = `<!doctype html>
  <html>
  <head>
    <title>회원가입</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
  </head>
  <body>
    <h1><a href="/">HOME</a></h1>
    <form action="/create_process" method="post">
      <p>
        <input type="text" name="id" placeholder="ID">
      </p>
      <p>
        <input type="password" name="pw" placeholder="PW">
      </p>
      <p>
        <input type="text" name="name" placeholder="이름">
      </p>
      <p>
        <input type="text" name="city" placeholder="지역">
      </p>
      <p>
        <input type="tel" name="phone" placeholder="휴대폰번호">
      </p>
      <p>
         <input type="submit">
      </p>
      </form>
  </body>
  </html>
  `
  response.writeHead(200);
  response.end(html);
}

exports.create_process = function(request,response){
  var body = '';
      request.on('data', function(data){
          body = body + data;
      });
      request.on('end', function(){
  var post = qs.parse(body);
          db.query(`INSERT INTO user (userid,pw,username,city,phone,created) VALUES (?,?,?,?,?,now());`,
          [post.id,post.pw,post.name,post.city,post.phone],function(error,result){
            if(error){
              throw error;
            }
            console.log(result.insertId);
            
            response.writeHead(302, {Location: `/`});
            response.end();
          })
});
}

exports.userpage = function(request,response){
  var body = '';
  request.on('data', function(data){
      body = body + data;
  });
  request.on('end', function(){
   var post = qs.parse(body);//data 수신
   var userid = post.id;
   var userpw = post.pw;
   
   console.log(post.clearprocess);
   console.log(userid,userpw);
   
  db.query(`SELECT * from user where userid='${userid}'AND pw='${userpw}'`,function(error,user){
    if(error){
      throw error;
    }
    /*db.query(`update user set work=1,ontime=now() where userid="${userid}"`,function(error,user){
      if(error){
        throw error;
      }});*/
    
    var id = user[0].id;
    db.query(`SELECT * from hospital where hs_user=${id} AND todayon=1 or makertodayon=1 order by hs_city`,function(error2,hospital){
      if(error2){
        throw error2;
      } 
      var chart = function chart1(hospital) {
        var list = `<table border = "1" style = "width : 300; height : 250"
        <tr>
        <th> 병원이름 </th> 
        <th> 전화번호 </th>
        <th> 비고 </th>
        <th> 병원주소 </th>
        <th> 해결여부 </th>
      </tr><br>`;
        
        var i = 0;
        while(i < hospital.length){
          var clear = function (hospital,i) {
            
            if(hospital[i].hs_clear === 0){
              return `
             
              <p><form action="/autologinprocess" method="post">
                <input type="hidden" id=1 name='hsid' value=${hospital[i].hs_id}>
                <input type="hidden" id=2 name='id' value=${userid}>
                <input type="hidden" id=3 name='pw' value=${userpw}>
                
                <input type="submit" value="미해결!">
              </form></p>`
              //<input type="hidden" id=4 name='clearprocess' value="0">
              

              ;
            }else{
              return `
              <p style="color:red">${hospital[i].finishtime.getHours()}:${hospital[i].finishtime.getMinutes()}:${hospital[i].finishtime.getSeconds()}</p>`;
            }
          }
          var note = function (hospital,i) {

            
          }
          list = list + 
          `<tr>
            <th> ${hospital[i].hs_name} </th> 
            <th> ${hospital[i].hs_phone} </th>
            <th> ${hospital[i].note} </th>
            <th> ${hospital[i].hs_address} </th>
            <th> ${clear(hospital,i)} </th>
          </tr>`
          i = i + 1;
        }
        list = list+'</table>';
        return list;
    }
    var chart = chart(hospital);
    var html = template.HTMLre(
      userid,
      ``,
      `<table border = "1" style = "width : 300; height : 250">
      <tr>
          <th> ${user[0].userid} </th>
          <th> ${user[0].username} </th>
          <th> ${user[0].city} </th>
          <th> ${user[0].phone} </th>
       </table>`+chart+`<script>
       function autorefresh(){  
             setTimeout('location.reload()',5000); 
       }
       autorefresh();
       </script>`,
      '/');


      //chart();
    response.writeHead(404);
      response.end(html);
    })});
   
    })
    }
    exports.clear_process = function (request,response) {
      var body = '';
      request.on('data', function(data){
      body = body + data;
      });
      request.on('end', function(){
      var post = qs.parse(body);
      console.log(post);
      console.log(post.hsid);
      console.log(post.id);
      console.log(post.pw);
     
      
      db.query(`UPDATE bestdb.hospital SET hs_clear=1 WHERE hs_id = ?;`,
      [post.hsid],function(error,result){
        if(error){
          throw error;
        }
        var gogo = topic.userpage(request,response);
        response.writeHead(302, {Location: `/?id=${post.id}`});
            response.end();
     
            
    })})
  }
exports.manager = function (request,response) {
  text = `texst`;
  list =`<form action="/manager_process" method="post">
      
        <select name="rider" id="rider-select">
        <option value="">--배달자를 입력하세요--</option>`; 
  db.query(`select * from user;`,function(error,user){
    
    if(error){
      throw error;
    }
    console.log(user.length);
    console.log(user[0]);
      var i = 0;
      
      while(i < user.length){
        console.log(user[i].userid)
        
          list = list + `
          <option value="${user[i].id}">${user[i].username}</option>`;
          i = i+1;
        }
        console.log(list);
        console.log(text);
        db.query(`select * from site order by sitename;`,function label (error,site){
          if(error){
            throw error;
          }

          j = 0;
          var label = `</select>`;
          console.log(site.length);
          while(j < site.length){
            
            label = label + `<p><label><input type="checkbox" name="city" value="${site[j].idsite}">${site[j].sitename}</label></p>`;
            j=j+1;
             
          };
          
    
          list= list+label+ `<p><input type="submit" value="Submit"> <input type="reset" value="Reset"></p></form>`;
          var html = template.HTMLforHS('manager', '배달기사',`${list}`,`/controlpage`);
  
          response.writeHead(200);
         response.end(html);
        });   
  }); 
}
exports.manager_process = function (request,response) {
  var body = '';
  request.on('data', function(data){
      body = body + data;
  });
  request.on('end', function(){
    var post = qs.parse(body);
  console.log(post.city+`시티`);
  console.log(post.city.length+`랭스`);
  var i = 0;
  var sql = ``;
  while(i < post.city.length){
    db.query(`UPDATE hospital set hs_user=${post.rider} where hs_city=${post.city[i]}`,function label (error,hospital){
      if(error){
        throw error;
      }});
      console.log(post.city[i]);
    //sql = sql + `UPDATE hospital set hs_user=${post.rider} where hs_id=${post.city[i]}`;
    i= i+1;
    
  }
  response.writeHead(302, {Location: `/manager`});
            response.end();
  })
}
exports.makerlogin = function(request,response){
  //var title = '로그인';
  var list = `
  <form name="login" action="/makerpage" method="post">
      <p>
        <input type="text" name="makername" placeholder="기공소이름">
      </p>
      <p>
        <input type="password" name="makerphone" placeholder="전화번호">
      </p>
            <p>
              <input type="submit" value="로그인">
            </p>
          </form>
        
 
  `;
  var control = `${control}`;
  var html = template.HTMLforHS(
    '로그인', 
    list,
    ``,
    `/makerlogin`
  );
  response.writeHead(200);
  response.end(html);
}

exports.makerpage = function(request,response){
  
    var body = '';
    request.on('data', function(data){
        body = body + data;
    });
    request.on('end', function(){
     var post = qs.parse(body);//data 수신
      console.log(post);
      db.query(`SELECT * from maker where makername='${post.makername}'AND makerphone='${post.makerphone}'`,function(error,maker){
        if(error){
          throw error;
        }
        
        db.query(`SELECT * from hospital left join maker on hospital.maker_id=maker.idmaker where maker_id=${maker[0].idmaker}`,function(error2,hospital){
         console.log(hospital);
         var i = 0;
         var list = `<form action="/makerpage_process" method="post">
                        <p>${hospital[0].makername}</p>
                        <table border = "1" style = "width : 300; height : 250">
                        <tr><th>병원이름</th><th>마지막으로 신청해주신 날짜</th></tr>`;
         
         while(i<hospital.length){
         list = list+ `<tr>
                        <th><label><input type="checkbox" name="maker" value="${hospital[i].hs_id}">${hospital[i].hs_name}</label></th>
                        <th>${hospital[i].makerlast.getMonth()+1}월${hospital[i].makerlast.getDate()}일${hospital[i].makerlast.getHours()}:${hospital[i].makerlast.getMinutes()}:${hospital[i].makerlast.getSeconds()}</th>
                      </tr>`;
         i = i+1;

         }
         list = list +`</table><p><input type="hidden" name="maker" value="-1"><input type="submit"></form></p>`;
         var html = template.HTMLforHS(
          '로그인', 
          list,
          ``,
          `/makerlogin`);
          response.writeHead(200);
          response.end(html);

})
})
}
)}
exports.makerpage_process = function (request,response) {
  var body = '';
  request.on('data', function(data){
      body = body + data;
  });
  request.on('end', function(){
    var post = qs.parse(body);
  var i = 0;
    console.log(post.maker.length);
    console.log(post);
    console.log(post.maker[0]);
  while(i < post.maker.length){
    db.query(`UPDATE hospital set makerlast=now(),makertodayon=1 where hs_id=${post.maker[i]}`,function label (error,hospital){
      if(error){
        throw error;
      }});
      console.log('포스트'+post.maker[i]);
      
    //sql = sql + `UPDATE hospital set hs_user=${post.rider} where hs_id=${post.city[i]}`;
    i= i+1;
    
  }
  response.writeHead(302, {Location: `/makerlogin`});
            response.end();
  })
}
exports.controlpage = function (request,response){
  var body = `<form action="/reset_clear" method="post">
                <input type="submit" value="배달기사해결초기화">
              </form><br>
              <form action="/reset_hs" method="post">
                <input type="submit" value="병원요청초기화">
              </form><br>
              <form action="/reset_maker" method="post">
                <input type="submit" value="기공소요청초기화">
              </form><br>
              <form action="/reset_all" method="post">
                <input type="submit" value="전체요청초기화">
              </form><br>

              <p><a href="/report_all">현황판</a></p>
              <p><a href="/manager">배달기사컨트롤</a></p><br>

              <p><a href="/ridermanager">배달기사관리</a></p>
              <p><a href="/sitemaker">지역생성</a></p>
              <p><a href="/makermaker">기공소생성</a></p>
              <p><a href="/hsmaker">병원생성</a></p><br>

              <p><a href="/makerlogin">기공소페이지</a></p>
              <p><a href="myhs">병원페이지</a></p>
              <p><a href="/">배달기사페이지</a></p>
              `
  var html = template.HTMLforHS('로그인', body,`최강배달`,`/controlpage`);
  response.writeHead(200);
          response.end(html);
}
exports.reset_clear = function(request,response){
  db.query(`UPDATE hospital set hs_clear=0`,function(error,maker){
    if(error){
      throw error;
    }
                var body = `<script type="text/javascript">alert("완료");
                            window.location.href="/controlpage";
                            </script>`;
                            var html = template.HTML('로그인', body,``,`최강배달`);
          response.writeHead(200);
          response.end(html);
  })
}
exports.reset_hs = function(request,response){
  db.query(`UPDATE hospital set todayon=0`,function(error,maker){
    if(error){
      throw error;
    }
                var body = `<script type="text/javascript">alert("완료");
                            window.location.href="/controlpage";
                            </script>`;
                            var html = template.HTML('로그인', body,``,`최강배달`);
          response.writeHead(200);
          response.end(html);
  })
}
exports.reset_maker = function(request,response){
  db.query(`UPDATE hospital set makertodayon=0`,function(error,maker){
    if(error){
      throw error;
    }
                var body = `<script type="text/javascript">alert("완료");
                            window.location.href="/controlpage";
                            </script>`;
                            var html = template.HTML('로그인', body,``,`최강배달`);
          response.writeHead(200);
          response.end(html);
  })
}
exports.reset_maker = function(request,response){
  db.query(`UPDATE hospital set makertodayon=0`,function(error,maker){
    if(error){
      throw error;
    }
                var body = `<script type="text/javascript">alert("완료");
                            window.location.href="/controlpage";
                            </script>`;
                            var html = template.HTML('로그인', body,``,`최강배달`);
          response.writeHead(200);
          response.end(html);
  })
}
exports.reset_all = function(request,response){
  db.query(`UPDATE hospital set makertodayon=0,todayon=0`,function(error,maker){
    if(error){
      throw error;
    }
                var body = `<script type="text/javascript">alert("완료");
                            window.location.href="/controlpage";
                            </script>`;
                            var html = template.HTML('로그인', body,``,`최강배달`);
          response.writeHead(200);
          response.end(html);
  })
}
exports.report_all = function(request,response){
  db.query(`select * from hospital left join maker on hospital.maker_id=maker.idmaker
                                    left join site on hospital.hs_city=site.idsite 
            order by hs_city `,function(error,hospital){
    if(error){
      throw error;
    }
    var list = `<table border = "1" style = "width : 300; height : 250">
                  <tr bgcolor="red">
                  <th> No.</th> 
                  <th> 삭제 </th>
                  <th> 지역 </th>
                    <th> 병원이름</th> 
                    <th> 병원전화번호</th>
                    <th> 병원주소 </th>
                    
                    <th> 기공소</th> 
                    
                    <th> 배달기사코드 </th>
                    <th> 해결여부 </th>
                    <th> 해결시각 </th>
                    <th> 병원요청 </th> 
                    <th> 병원요청시각 </th>
                    <th> 기공소요청 </th>
                    <th> 기공소요청시각 </th>
                   
                  </tr>`;
    var i = 0;
    while(i<hospital.length){
      var bcolor = ``;
      if(hospital[i].todayon===1){
        bcolor = `bgcolor="red"`;
        }else if(hospital[i].makertodayon === 1){
          bcolor = `bgcolor="red"`;
        }
      var deletebutton = `<form action="/hsdelete" method="post">
                                  <input type="hidden" name="hs_id" value="${hospital[i].hs_id}">
                                  <input type="submit" value="삭제">
                          </form>`;
      list = list+`<tr>
      <th> ${[i]} </th> 
      <th> ${deletebutton} </th>
      <th> ${hospital[i].sitename} </th> 
            <th ${bcolor} > ${hospital[i].hs_name}(${hospital[i].hs_id}) </th>            
            <th> ${hospital[i].hs_phone} </th>
            <th> ${hospital[i].hs_address} </th>
            <th> ${hospital[i].makername} </th> 
            
            <th> ${hospital[i].hs_user} </th>
            <th> ${hospital[i].hs_clear} </th>
            <th> ${hospital[i].finishtime.getMonth()+1}월${hospital[i].finishtime.getDate()}일${hospital[i].finishtime.getHours()}:${hospital[i].finishtime.getMinutes()}:${hospital[i].finishtime.getSeconds()} </th>
            <th> ${hospital[i].todayon} </th> 
            <th> ${hospital[i].lasttodayon.getMonth()+1}월${hospital[i].lasttodayon.getDate()}일${hospital[i].lasttodayon.getHours()}:${hospital[i].lasttodayon.getMinutes()}:${hospital[i].lasttodayon.getSeconds()} </th>
            <th> ${hospital[i].makertodayon} </th>
            <th> ${hospital[i].makerlast.getMonth()+1}월${hospital[i].makerlast.getDate()}일${hospital[i].makerlast.getHours()}:${hospital[i].makerlast.getMinutes()}:${hospital[i].makerlast.getSeconds()} </th>
            
          </tr>`;
      i= i+1;
    }
    list = list+`</table>`;
    var html = template.HTMLforHS('로그인',`<meta http-equiv="refresh" content="5">`,list,`/controlpage`);
          response.writeHead(200);
          response.end(html);

  })
}
exports.hsdelete = function(request,response){
  var body = '';
  request.on('data', function(data){
      body = body + data;
  });
  request.on('end', function(){
    var post = qs.parse(body);
    console.log(post.hs_id);
  db.query(`delete from hospital where hs_id=${post.hs_id}`,function(error,maker){
    if(error){
      throw error;
    }
                var body = `<script type="text/javascript">alert("완료");
                            window.location.href="/report_all";
                            </script>`;
                            var html = template.HTMLforHS('로그인', body,``,`/constolpage`);
          response.writeHead(200);
          response.end(html);
  })
})
}
exports.sitemaker = function(request,response){
  db.query(`select * from site order by sitename`,function(error,site){
  var body = `<form action="/sitemaker_process" method="post">
                <input type="text" id="city" name="city"><br><br>
                <input type="submit" value="생성">
                <p>---------------------------------</p>
              </form><br><table border="1px solid">`;

  i = 0;
  while(i < site.length){
    body = body+`<tr>
                    <th>${site[i].sitename}</th>
                    <th> <form action="site_delete" method="post">
                          <input type="hidden" name="idsite" value="${site[i].idsite}">
                          <input type="submit" value="삭제">
                          </form>
                    </th>
                </tr>`;
                i=i+1;
  }
  body = body+`</form>`;

  
              var html = template.HTMLforHS('로그인', body,``,`/controlpage`);
          response.writeHead(200);
          response.end(html);

})
}
exports.sitemaker_process = function(request,response){
  var body = '';
  request.on('data', function(data){
      body = body + data;
  });
  request.on('end', function(){
   var post = qs.parse(body);//data 수신
   console.log(post);
   db.query(`insert into site (sitename) values("${post.city}")`,function(error,maker){
    if(error){
      throw error;}
                var body = `<script type="text/javascript">alert("완료");
                            window.location.href="/sitemaker";
                            </script>`;
                            var html = template.HTMLforHS('로그인', body,``,`/constolpage`);
          response.writeHead(200);
          response.end(html);
  })
  
  })
}
exports.site_delete = function(request,response){
  var body = '';
  request.on('data', function(data){
      body = body + data;
  });
  request.on('end', function(){
   var post = qs.parse(body);//data 수신
   console.log(post);
   db.query(`delete from site where idsite=${post.idsite}`,function(error,maker){
    if(error){
      throw error;}
                var body = `<script type="text/javascript">alert("완료");
                            window.location.href="/sitemaker";
                            </script>`;
                            var html = template.HTMLforHS('로그인', body,``,`/sitemaker`);
          response.writeHead(200);
          response.end(html);
  })
})
}
exports.ridermanager = function(request,response){
  db.query(`select * from user`,function(error,site){
  var body = `<table border="1px solid"
                <tr>
                <th>NO</th>
                <th>ID</th>
                <th>PW</th>
                <th>이름</th>
                <th>지역</th>
                <th>전화번호</th>
                <th>생성일</th>
                <th>삭제</th>
                </tr>`;

  i = 0;
  while(i < site.length){
    body = body+`<tr>
                    <th>${i}</th>
                    <th>${site[i].userid}</th>
                    <th>${site[i].pw}</th>
                    <th>${site[i].username}</th>
                    <th>${site[i].city}</th>
                    <th>${site[i].phone}</th>
                    <th>${site[i].created.getMonth()}월${site[i].created.getDate()}일${site[i].created.getHours()}:${site[i].created.getMinutes()}:${site[i].created.getSeconds()}</th>
                    <th> <form action="ridermanager_delete" method="post">
                          <input type="hidden" name="idsite" value="${site[i].id}">
                          <input type="submit" value="삭제">
                          </form>
                    </tr>`;
                i=i+1;
  }
  body = body+`</form>`;

  
              var html = template.HTMLforHS('로그인', body,``,`/controlpage`);
          response.writeHead(200);
          response.end(html);

})
}
exports.ridermanager_delete = function(request,response){
  var body = '';
  request.on('data', function(data){
      body = body + data;
  });
  request.on('end', function(){
   var post = qs.parse(body);//data 수신
   console.log(post);
   db.query(`delete from user where id=${post.idsite}`,function(error,maker){
    if(error){
      throw error;}
                var body = `<script type="text/javascript">alert("완료");
                            window.location.href="/ridermanager";
                            </script>`;
                            var html = template.HTMLforHS('로그인', body,``,`/ridermanager`);
          response.writeHead(200);
          response.end(html);
  })
})
}
exports.autologinprocess = function(request,response){
  var body = '';
  request.on('data', function(data){
      body = body + data;
  });
  request.on('end', function(){
   var post = qs.parse(body);//data 수신
    db.query(`UPDATE bestdb.hospital SET hs_clear=1,finishtime = now() WHERE hs_id = ?;`,
    [post.hsid],function(error,result){
      if(error){
        throw error;
      }});
   
 var k = ` <form name="login" action="/userlogin" method="post">
        <input type="hidden" name="id" value="${post.id}">
        <input type="hidden" name="pw" value="${post.pw}">  
          </form>

          <script type="text/javascript">
          document.login.submit();
          </script>`;
  var html = template.HTMLforHS('로그인', k,``,`/ridermanager`);
          response.writeHead(200);
          response.end(html);
})}

  
/*
exports.home = function(request,response){
db.query('SELECT * from topic',function(error,topics){
    var title = 'Welcome';
    var description = 'Hello, Node.js';
    var list = template.list(topics);
    var html = template.HTML(title, list,
      `<h2>${title}</h2>${description}`,
      `<a href="/create">create</a>`
    );
    response.writeHead(200);
    response.end(html);
  });
}

exports.page = function(request,response){
    var _url = request.url;
    var queryData = url.parse(_url, true).query;
    var pathname = url.parse(_url, true).pathname;
    db.query('SELECT * from topic',function(error,topics){
        if(error){
          throw error;
        }
        db.query(`SELECT * FROM topic left join author on topic.author_id=author.id WHERE topic.id=?`,[queryData.id],function(error2, topic){
         if(error2){
            throw error2;
          }
         console.log(topic);
       var title = topic[0].title;
       var description = topic[0].description;
       var list = template.list(topics);
       var html = template.HTML(title, list,
         `<h2>${title}</h2>
         ${description}
         <p>by ${topic[0].name}</p>`,
         `<a href="/create">create</a>
         <a href="/update?id=${queryData.id}">update</a>
                 <form action="delete_process" method="post">
                   <input type="hidden" name="id" value="${queryData.id}">
                   <input type="submit" value="delete">
                 </form>`
       );
       response.writeHead(200);
       response.end(html);
        })   
     });
}

exports.create = function(request,response){
    db.query('SELECT * from topic',function(error,topics){
        db.query(`select * from author`,function(error,authors){
          var title = 'create';
          var list = template.list(topics);
          var html = template.HTML(title, list,
            `<form action="/create_process" method="post">
            <p><input type="text" name="title" placeholder="title"></p>
            <p>
              <textarea name="description" placeholder="description"></textarea>
            </p>
            <p>
             ${template.authorselect(authors)}
            </p>
            <p>
              <input type="submit">
            </p>
          </form>`,
            `<a href="/create">create</a>`
          );
          response.writeHead(200);
          response.end(html);
        });    
      });
}

exports.create_process = function(request,response){
    var body = '';
      request.on('data', function(data){
          body = body + data;
      });
      request.on('end', function(){
          var post = qs.parse(body);
          db.query(`insert into topic (title, description, created, author_id) values(?,?,now(),?)`,
          [post.title,post.description,post.author],function(error,result){
            if(error){
              throw error;
            }
            console.log(result.insertId);
            response.writeHead(302, {Location: `/?id=${result.insertId}`});
            response.end();
          })
      });
}

exports.update = function(request,response){
    var _url = request.url;
    var queryData = url.parse(_url, true).query;
    var pathname = url.parse(_url, true).pathname;
    db.query(`select * from topic`,function(error,topics){
        if(error){
          throw error;
        }
       db.query(`SELECT * FROM topic WHERE id=?`,[queryData.id],function(error2, topic){
         if(error2){
           throw error2;
         }
         db.query(`select * from author`,function(error2,authors){
           var list = template.list(topics);
           console.log('토픽아이디'+topic[0].id);
           var html = template.HTML(topic[0].title, list,
             `
             <form action="/update_process" method="post">
               <input type="hidden" name="id" value="${topic[0].id}">
               <p><input type="text" name="title" placeholder="title" value="${topic[0].title}"></p>
               <p>
                 <textarea name="description" placeholder="description">${topic[0].description}</textarea>
               </p>
               <p>
                 ${template.authorselect(authors,topic[0].author_id)}
               </p>
               <p>
                 <input type="submit">
               </p>
             </form>
             `,
             `<a href="/create">create</a> <a href="/update?id=${topic[0].id}">update</a>`
           );         
           response.writeHead(200);
           response.end(html);
         });
         });
       });
}
exports.update_process = function(request,response){
    var body = '';
    request.on('data', function(data){
        body = body + data;
    });
    request.on('end', function(){
        var post = qs.parse(body);
        var id = post.id;
        var title = post.title;
        var description = post.description;
        db.query(`update topic set title=?, description=?, author_id=? where id=?`,[post.title,post.description,post.author,post.id],function(error,result){
          response.writeHead(302, {Location: `/?id=${post.id}`});
            response.end();
        })
    });    
}
exports.delete_process = function(request,response){
    var body = '';
      request.on('data', function(data){
          body = body + data;
      });
      request.on('end', function(){
          var post = qs.parse(body);
          db.query(`delete from topic where id=?`,[post.id],function(error,result){
            if(error){
              throw error
            }
            response.writeHead(302, {Location: `/`});
            response.end();
          })
      });    
}*/