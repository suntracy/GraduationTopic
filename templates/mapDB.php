<?php
require_once "connect.php";
$sql_query = "select * from hospital";
$result = mysqli_query($link, $sql_query); 

if ($result) { 
    if (mysqli_num_rows($result) > 0) {  
        $queryData = mysqli_fetch_all($result, MYSQLI_NUM);
        mysqli_free_result($result);
        echo json_encode($queryData, JSON_NUMERIC_CHECK);
    } else {
        echo "null";
    }
} else {
    echo "查詢錯誤: " . mysqli_error($db->link);
}


mysqli_close($link);
?>