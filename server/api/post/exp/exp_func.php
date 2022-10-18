<?php 

include '../mtx/mtx_func.php';
include '../level/level_func.php';

function add_exp($exp, $usr, $token) {

    global $conn;

    $sql="SELECT exp FROM users WHERE username='$usr' AND token='$token'";
    $result=mysqli_query($conn, $sql);
    $row=mysqli_fetch_assoc($result);

    $nexp=$row['exp'];
    $exp=$nexp+$exp;

    if ($exp >= 10000) {
        add_lvl(1, $usr, $token);

        $exp=$exp-10000;
        
        $sql="UPDATE users SET exp='$exp' WHERE username='$usr' AND token='$token'";
        $result=mysqli_query($conn, $sql);

        if ($result==TRUE) {} else {
            
            echo json_encode("nope", JSON_PRETTY_PRINT);
        }

    } else {

        $sql="UPDATE users SET exp='$exp' WHERE username='$usr' AND token='$token'";
        $result=mysqli_query($conn, $sql);

        if ($result==TRUE) {
            
            

        } else {
            
            echo json_encode("nope", JSON_PRETTY_PRINT);
        }
    }
}

function del_exp($exp, $usr, $token) {

    global $conn;

    $sql="SELECT exp FROM users WHERE username='$usr' AND token='$token'";
    $result=mysqli_query($conn, $sql);
    $row=mysqli_fetch_assoc($result);

    $nexp=$row['exp'];
    $exp=$nexp-$exp;

    $sql="UPDATE users SET exp='$exp' WHERE username='$usr' AND token='$token'";
    $result=mysqli_query($conn, $sql);

    if ($result==TRUE) {
        
        

    } else {
        
        echo json_encode("nope", JSON_PRETTY_PRINT);
    }
}

?>