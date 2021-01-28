var http = require('http');
var url = require('url');
var qs = require('querystring');
var template = require('./lib/template.js');
var db = require('./lib/db');
var topic = require('./lib/topic');
var hsmn = require('./lib/hsmn');
const { SSL_OP_TLS_BLOCK_PADDING_BUG } = require('constants');

var app = http.createServer(function(request,response){
    var _url = request.url;
    var queryData = url.parse(_url, true).query;
    var pathname = url.parse(_url, true).pathname;
    if(pathname === '/'){
      if(queryData.id === undefined){
        topic.login(request,response);
      }else if(pathname === '/create'){
        topic.login(request,response);
      }
    
    
    }else if(pathname === '/create'){
      topic.create(request,response);
    }else if(pathname === '/create_process'){
      topic.create_process(request,response);
    }else if(pathname === '/userlogin'){
      topic.userpage(request,response);
    }else if(pathname === '/clear_process'){
      topic.clear_process(request,response);
    }else if(pathname === '/userinterpace'){
      topic.userinterpace(post);
    }else if(pathname === '/hsmaker'){
      hsmn.hsmaker(request,response);
    }else if(pathname === '/hsmaker_process'){
      hsmn.hsmaker_process(request,response);
    }else if(pathname === '/manager'){
      topic.manager(request,response);
    }else if(pathname === '/manager_process'){
      topic.manager_process(request,response);
    }else if(pathname === '/myhs'){
      hsmn.myhs(request,response);
    }else if(pathname === '/myhs_process'){
      hsmn.myhs_process(request,response);
    }else if(pathname === '/makermaker'){
      hsmn.makermaker(request,response);
    }else if(pathname === '/makermaker_process'){
      hsmn.makermaker_process(request,response);
    }else if(pathname === '/makerlogin'){
      topic.makerlogin(request,response);
    }else if(pathname === '/makerpage'){
      topic.makerpage(request,response);
    }else if(pathname === '/makerpage_process'){
      topic.makerpage_process(request,response);
    }else if(pathname === '/controlpage'){
      topic.controlpage(request,response);
    }else if(pathname === '/reset_clear'){
      topic.reset_clear(request,response);
    }else if(pathname === '/reset_hs'){
      topic.reset_hs(request,response);
    }else if(pathname === '/reset_maker'){
      topic.reset_maker(request,response);
    }else if(pathname === '/reset_all'){
      topic.reset_all(request,response);
    }else if(pathname === '/report_all'){
      topic.report_all(request,response);
    }else if(pathname === '/hsdelete'){
      topic.hsdelete(request,response);
    }else if(pathname === '/sitemaker'){
      topic.sitemaker(request,response);
    }else if(pathname === '/sitemaker_process'){
      topic.sitemaker_process(request,response);
    }else if(pathname === '/site_delete'){
      topic.site_delete(request,response);
    }else if(pathname === '/ridermanager'){
      topic.ridermanager(request,response);
    }else if(pathname === '/ridermanager_delete'){
      topic.ridermanager_delete(request,response);
    }else if(pathname === '/autologinprocess'){
      topic.autologinprocess(request,response);
    }                      
                          
    
    
    
    
    
    else {
      response.writeHead(404);
      response.end('Not found1');
    }
});
app.listen(3000);