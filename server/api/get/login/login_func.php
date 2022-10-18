<?php

function login($usr, $pass, $token) {

    global $conn;

    $sql="SELECT status FROM users WHERE username='$usr' AND password='$pass' AND token='$token'";
    $result=mysqli_query($conn, $sql);

    if (mysqli_num_rows($result)!=0) {
        $row=mysqli_fetch_assoc($result);

        if ($row['status']=="normal") {

            echo json_encode("ok", JSON_PRETTY_PRINT);

        } else {

            echo json_encode("ban", JSON_PRETTY_PRINT);

        }

    } else {

        echo json_encode("nope", JSON_PRETTY_PRINT);

    }
    
}

?>