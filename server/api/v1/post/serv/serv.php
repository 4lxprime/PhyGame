<?php

date_default_timezone_set('UTC');
$urlkey=htmlspecialchars($_GET['urlkey']);
$srv_ip=htmlspecialchars($_GET['ip']);
$srv_port=htmlspecialchars($_GET['port']);
$class=htmlspecialchars($_GET['class']);
$key="VEIDVOE9oN8O3C4TnU2RIN1O0rF82mU6RuJwHFQ6GH5mF4NQ3pZ8Z6R7A8dL0";

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header("Access-Control-Allow-Headers: X-Requested-With");

?>

<?php

include 'serv_func.php';
include '../../global_func.php';
include '../../db/db_conn.php';

if ($urlkey===$key) {

    addServ($srv_ip, $srv_port, $class);

} else {

    echo json_encode("bad_key", JSON_PRETTY_PRINT);

}

?>