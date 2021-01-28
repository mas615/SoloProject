var db = require('./db');
var template = require('./template좇망.js');
var url = require('url');
var qs = require('querystring');

var http = require('http');
var url = require('url');
var qs = require('querystring');


exports.home = function(request,response){
  var html =`
  <!doctype html>
  <html>
  <head>
    <title>WEB1 - </title>
    <meta charset="utf-8">
  </head>
  <body>
  <form action="/create_process" method="post">
      <p>
        <input type="text" name="id" placeholder="ID">
      </p>
      <p>
        <input type="text" name="pw" placeholder="PW">
      </p>
            <p>
              <input type="submit">
            </p>
          </form>
        <h1><a href="/create">회원가입</a></h1>
  </body>
  </html>
  `
    response.writeHead(200);
    response.end(html);
  
};

exports.create_user = function(request,response){
  console.log(111111);
  template.HTML('createuser',
    `<form action="/create_process" method="post">
  <p>
    <input type="text" name="id" placeholder="ID">
  </p>
  <p>
    <input type="text" name="pw" placeholder="PW">
  </p>
        <p>
          <input type="submit"></input>
          `);
          
    
          
}

/*exports.page = function(request,response){
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