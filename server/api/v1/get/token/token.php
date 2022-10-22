<?php
date_default_timezone_set('UTC');
$urlkey=htmlspecialchars($_GET['urlkey']);
$pass=htmlspecialchars($_GET['passwd']);
$usr=htmlspecialchars($_GET['usrnm']);
$action=htmlspecialchars($_GET['action']);
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
include 'token_func.php';
include '../../global_func.php';
include '../../db/db_conn.php';
?>

<?php 
if ($urlkey===$key) {
    $sql="SELECT password FROM users WHERE username='$usr' AND password='$pass'";
    $result=mysqli_query($conn, $sql);

    if (mysqli_num_rows($result)!=0) {
        $row=mysqli_fetch_assoc($result);

        if ($row['password']===$pass) {

            if ($action==="get_token") {
                token_get($usr, $pass);

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