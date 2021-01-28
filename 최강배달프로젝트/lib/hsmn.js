var db = require('./db');
var template = require('./template.js');
var topic = require('./topic.js');
var url = require('url');
var qs = require('querystring');
var hsmn = require('./hsmn');

exports.hsmaker = function (request,response) {
  db.query(`select * from site order by sitename`,function(error,site){
    console.log(site);
    console.log(site.length);
    i = 0;
    var city =`<select name="hs_city" id="pet-select">`;

      while(i < site.length){
        city = city +`<option value="${site[i].idsite}">${site[i].sitename}</option>`;
        i=i+1;
      };

    city = city+`</select>`;

    var body = `<form action="/hsmaker_process" method="post">
    <p>
      <input type="text" name="hs_name" placeholder="병원이름">
    </p>
    <p>
      <input type="text" name="hs_address" placeholder="병원주소">
    </p>
    <p>
      <input type="text" name="maker_id" placeholder="기공소">
    </p>
    <p>
     ${city}
      
    </p>
    <p>
      <input type="tel" name="hs_phone" placeholder="전화번호">
    </p>
    <p>
    비고<br>
    <textarea name="note" cols="23" rows="8" ></textarea>
    </p>
    <p>
       <input type="submit">
    </p>
    </form>`;

    var html = template.HTMLforHS('매니저','병원매니저',body,'/controlpage');
    response.writeHead(200);
    response.end(html);
  })
}
exports.hsmaker_process = function (request,response){
    var body = '';
      request.on('data', function(data){
          body = body + data;
      });
      request.on('end', function(){
  var post = qs.parse(body);
  console.log(post.hs_name);
  response.writeHead(302, {Location: `/hsmaker`});
            response.end();
          db.query(`INSERT INTO hospital (hs_name, hs_address, hs_clear, maker_id, hs_city, hs_user, hs_phone,note) VALUES (?, ?, 0, ?, ?, ?, ?,?);`,
          [post.hs_name,post.hs_address,post.maker_id,post.hs_city,post.hs_user,post.hs_phone,post.note],function(error,result){
            if(error){
              throw error;
            }
            console.log(result.insertId);
            response.writeHead(302, {Location: `/hsmaker`});
            response.end();
          })
});

}
exports.hsconnectuser = function (request,response) {
    db.query('SELECT * from topic',function(error,topics){
        if(error){
            throw error;
        }
        var select = function (topics) {
            
        }
    `<form>
    <select name="color">
      <option value="서버에 전송될 값">red</option>
      <option value="blue">blue</option>
    </select>
    <select name="color2" multiple>
      <option value="black">검은색</option>
      <option value="blue">파란색</option>
    </select>
  </form>
    `
    });
    
    
}
exports.myhs = function (request,response) {
    var body = `<form action="/myhs_process" method="post">
    <p>
      <input type="text" name="hs_name" placeholder="병원코드">
    </p>
    
    <h7>보낼 물건 있나요?</h7><br>
      <label><input type="radio" name="todayon" value="1" checked>있어요</label>
      <label><input type="radio" name="todayon" value="0">없어요</label>

    <p>
       <input type="submit">
    </p>
    
    </form>`;
  var html = template.HTMLforHS('최강배달','<h1>최강배달병원매니저</h1>',body,'/myhs');
    response.writeHead(200);
    response.end(html);
    
}
exports.myhs_process = function (request,response) {
    var body = '';
      request.on('data', function(data){
          body = body + data;
      });
      request.on('end', function(){
  var post = qs.parse(body);
  console.log(post);
  db.query(`UPDATE hospital SET todayon = ?,lasttodayon = now() WHERE hs_id =?;`,
          [post.todayon,post.hs_name],function(error,result){
            if(error){
              throw error;
            }
            var body = `<p>병원코드:${post.hs_name}</p><p>정상처리되었습니다.</P>`
            var html = template.HTMLforHS('최강배달','<h1>최강배달병원매니저</h1>',body,'/myhs');
            response.writeHead(200);
            response.end(html);
          })
    
});
}
exports.makermaker = function (request,response) {
    var body = `<form action="/makermaker_process" method="post">
    <p>
      <input type="text" name="makername" placeholder="기공소이름">
    </p>
    <p>
      <input type="text" name="makeraddress" placeholder="기공소주소">
    </p>
    <p>
      <input type="text" name="makerphone" placeholder="기공전화번호">
    </p>
    <p>
    비고<br>
    <textarea name="makernote" cols="23" rows="8" ></textarea>
    </p>
    <p>
       <input type="submit">
    </p>
    </form>`
    var html = template.HTMLforHS('매니저','기공소매니저',body,'/controlpage');
    response.writeHead(200);
    response.end(html);

}
exports.makermaker_process = function (request,response){
    var body = '';
      request.on('data', function(data){
          body = body + data;
      });
      request.on('end', function(){
  var post = qs.parse(body);
  console.log(post.hs_name);
  response.writeHead(302, {Location: `/makermaker`});
            response.end();
          db.query(`INSERT INTO maker (makername, makeraddress, makerphone, makernote) VALUES (?,?,?,?);`,
          [post.makername,post.makeraddress,post.makerphone,post.makernote],function(error,result){
            if(error){
              throw error;
            }
            console.log(result.insertId);
            response.writeHead(302, {Location: `/hsmaker`});
            response.end();
          })
});}
/* exports.ggmaker = function (request,response) {
    var body = `<form action="/hsmaker_process" method="post">
    <p>
      <input type="text" name="hs_name" placeholder="병원이름">
    </p>
    <p>
      <input type="text" name="hs_address" placeholder="병원주소">
    </p>
    <p>
      <input type="text" name="maker_id" placeholder="기공소">
    </p>
    <p>
      <input type="text" name="hs_city" placeholder="지역">
    </p>
    <p>
      <input type="tel" name="hs_phone" placeholder="전화번호">
    </p>
    <p>
       <input type="submit">
    </p>
    </form>`
    var html = template.HTML('매니저','병원매니저',body,'병원매니저');
    response.writeHead(200);
    response.end(html);

}
exports.ggmaker_process = function (request,response){
    var body = '';
      request.on('data', function(data){
          body = body + data;
      });
      request.on('end', function(){
  var post = qs.parse(body);
  console.log(post.hs_name);
  response.writeHead(302, {Location: `/ggmaker_process`});
            response.end();
          db.query(`INSERT INTO hospital (hs_name, hs_address, hs_clear, maker_id, hs_city, hs_user, hs_phone) VALUES (?, ?, 0, ?, ?, ?, ?);`,
          [post.hs_name,post.hs_address,post.hs_maker_id,post.hs_city,post.hs_user,post.hs_phone],function(error,result){
            if(error){
              throw error;
            }
            console.log(result.insertId);
            response.writeHead(302, {Location: `/hsmaker`});
            response.end();
          })
});

}*/