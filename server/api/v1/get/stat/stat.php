<?php
date_default_timezone_set('UTC');
$usr=htmlspecialchars($_GET['usrnm']);
$action=htmlspecialchars($_GET['action']);
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header("Access-Control-Allow-Headers: X-Requested-With");
?>

<?php

include 'stat_func.php';
include '../../global_func.php';
include '../../db/db_conn.php';

?>

<?php 

if ($action==="get_kill") {
    get_kill($usr);

} else {

    echo json_encode("error", JSON_PRETTY_PRINT);

}

?>