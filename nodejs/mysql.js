var mysql      = require('mysql');//mysql모듈을 사용하겠다 그리고 그모듈은 mysql이라는 변수에 넣는다.
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : '111111',
  database : 'opentutorials'
});
 
connection.connect();
 
connection.query('SELECT * from topic', function (error, results, fields) {
  if (error) {
      console.log(error);
    }
  console.log(results);
});
 
connection.end();