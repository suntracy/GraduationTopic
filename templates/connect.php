<?php
header("Content-Type:text/html; charset=utf-8");
define('DB_Server', 'localhost');       //資料庫主機
define('DB_User', 'root');              //資料庫使用者
define('DB_Password', '');              //資料庫使用者密碼
define('DB_Database', 'scankin');       //資料庫名稱
//資料庫連接
$link = mysqli_connect(DB_Server, DB_User, DB_Password, DB_Database);
// $link = mysqli_connect("localhost", "root", "", "test");
/* 檢查是否連接失敗 */
if (!$link) {
    die("連接失敗" . mysqli_connect_error()); //輸出資料庫連接錯誤
} else {
    // echo "Success!!!<br>";  //輸出資料庫連接成功
}

mysqli_set_charset($link, "utf8");

?>