<?php
date_default_timezone_set('UTC');
$urlkey=htmlspecialchars($_GET['urlkey']);
$token=htmlspecialchars($_GET['token']);
$pass=htmlspecialchars($_GET['passwd']);
$usr=htmlspecialchars($_GET['usrnm']);
$action=htmlspecialchars($_GET['action']);
$mtx=htmlspecialchars($_GET['mtx']);
$token=hash('sha256', $token);
$token=hash('sha512', $token);
$pass=hash('sha256', $pass);
$pass=hash('sha512', $pass);
$key="VEIDVOE9oN8O3C4TnU2RIN1O0rF82mU6RuJwHFQ6GH5mF4NQ3pZ8Z6R7A8dL0";
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header("Access-Control-Allow-Headers: X-Requested-With");
$ip=$_SERVER['REMOTE_ADDR'];
?>

<?php
include 'mtx_func.php';
include '../../global_func.php';
include '../../db/db_conn.php';
?>

<?php 

if ($urlkey===$key) {
    $sql="SELECT token FROM users WHERE username='$usr' AND password='$pass'";
    $result=mysqli_query($conn, $sql);

    if (mysqli_num_rows($result)!=0) {
        $row=mysqli_fetch_assoc($result);

        if ($row['token']===$token) {

            if ($action==="get_mtx") {
                get_mtx($mtx, $usr);

            } else if ($action==="del_mtx") {
                del_mtx($mtx, $usr);

            } else if ($action==="create_account") {

                create_acc($pass, $usr, $ip);

            } else {

                echo json_encode("error", JSON_PRETTY_PRINT);

            }

        } else {
            
            echo json_encode("nope", JSON_PRETTY_PRINT);
        }

    } else {

        if ($action==="create_account") {
            create_acc($pass, $usr, $ip);

        } else {

            echo json_encode("bad_logins", JSON_PRETTY_PRINT);

        }
    }

} else {
    
    echo json_encode("bad_key", JSON_PRETTY_PRINT);
}

?>