const { HTML } = require("./template");

module.exports = {
  HTML:function(title,body){
    console.log(12345);
    return`
        <!doctype html>
    <html>
    <head>
      <title>${title}</title>
      <meta charset="utf-8">
    </head>
    <body>
      <h1><a href="/">HOME</a></h1>
      ${body}
    </body>
    </html>
    `;
   
  }

}