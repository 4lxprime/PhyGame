<?php

function add_lvl($level, $usr, $token) {

    global $conn;

    $sql="SELECT level FROM users WHERE username='$usr' AND token='$token'";
    $result=mysqli_query($conn, $sql);
    $row=mysqli_fetch_assoc($result);

    $nlevel=$row['level'];
    $level=$nlevel+$level;

    $sql="UPDATE users SET level='$level' WHERE username='$usr' AND token='$token'";
    $result=mysqli_query($conn, $sql);

    if ($result==TRUE) {
        
        echo json_encode("ok", JSON_PRETTY_PRINT);

    } else {
        
        echo json_encode("nope", JSON_PRETTY_PRINT);
    }

}

function del_lvl($level, $usr, $token) {

    global $conn;

    $sql="SELECT level FROM users WHERE username='$usr' AND token='$token'";
    $result=mysqli_query($conn, $sql);
    $row=mysqli_fetch_assoc($result);

    $nlevel=$row['level'];
    $level=$nlevel-$level;
    
    $sql="UPDATE users SET level='$level' WHERE username='$usr' AND token='$token'";
    $result=mysqli_query($conn, $sql);

    if ($result==TRUE) {
        
        echo json_encode("ok", JSON_PRETTY_PRINT);

    } else {
        
        echo json_encode("nope", JSON_PRETTY_PRINT);
    }

}

?>