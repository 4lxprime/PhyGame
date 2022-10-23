<?php

function sendD($usr, $top) {
    
    $url="https://discord.com/api/webhooks/";
    $headers=['Content-Type: application/json; charset=utf-8'];
    $post=['username' => 'Nocturno '.$top, 'content' => 'GG a '.$usr.' pour son '.$top.' !'];
    $ch=curl_init();

    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($post));

    curl_exec($ch);

}

function create_acc($pass, $usr, $ip) {

    global $conn;

    $sql="SELECT ip FROM users WHERE ip='$ip'";
    $result=mysqli_query($conn, $sql);

    if (mysqli_num_rows($result)!=0) {

        if (mysqli_num_rows($result)>=4) {

            echo json_encode("max_account_reached", JSON_PRETTY_PRINT);

        } else {

            if ($pass==="") {
            
                echo json_encode("bad_password", JSON_PRETTY_PRINT);
        
            } else {
                $actdate=date('Y-m-d H:i:s');
                $sql="INSERT INTO users (username, password, status, date, ip, kills) VALUES ('$usr', '$pass', 'normal', '$actdate', '$ip', '0')";
                $result=mysqli_query($conn, $sql);
        
                if ($result==TRUE) {
        
                    echo json_encode("ok", JSON_PRETTY_PRINT);
        
                }

            }
    
        }

    } else {

        if ($pass==="") {
            
            echo json_encode("bad_password", JSON_PRETTY_PRINT);
    
        } else {
            $actdate=date('Y-m-d H:i:s');
            $sql="INSERT INTO users (username, password, status, date, ip) VALUES ('$usr', '$pass', 'normal', '$actdate', '$ip')";
            $result=mysqli_query($conn, $sql);
    
            if ($result==TRUE) {
    
                echo json_encode("ok", JSON_PRETTY_PRINT);
    
            }

        }

    }

}

?>