<?php

function generateToken($usr) {
    $lenght=20;
    $usr=base64_encode($usr);
    $char='0123456789azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN';
    $maxlenght=strlen($char);
    $randomstring='';
    for ($i = 0; $i < $lenght; $i++) {
        $randomstring .= $char[rand(0, $maxlenght - 1)];
    }
    return "PHYGAMEISBETTER-".$usr."-".$randomstring;
}

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

    $response=curl_exec($ch);

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
                $sql="INSERT INTO users (username, password, mtx, status, date, ip, level, exp) VALUES ('$usr', '$pass', '500', 'normal', '$actdate', '$ip', '1', '1')";
                $result=mysqli_query($conn, $sql);
        
                if ($result==TRUE) {
                    $tokn=generateToken($usr);
                    $tkn=hash('sha256', $tokn);
                    $tkn=hash('sha512', $tkn);
                    $sql="INSERT INTO stat (top1, top10, top25, username, token) VALUES ('0', '0', '0', '$usr', '$tkn')";
                    $result=mysqli_query($conn, $sql);
        
                    if ($result==TRUE) {
                        $sql="UPDATE users SET token='$tkn' WHERE username='$usr' AND password='$pass'";
                        $result=mysqli_query($conn, $sql);
        
                        if ($result==TRUE) {
                            
                            $sql="INSERT INTO token (token, password) VALUES ('$tokn', '$pass')";
                            $result=mysqli_query($conn, $sql);
        
                            if ($result==TRUE) {
        
                                echo json_encode("$tokn", JSON_PRETTY_PRINT);
        
                            } else {
        
                                echo json_encode("error_creating_account_token_table", JSON_PRETTY_PRINT);
                            }
        
                        } else {
                            
                            echo json_encode("error_creating_account_stat", JSON_PRETTY_PRINT);
                        }
                    } else {
                        
                        echo json_encode("error_creating_account_token", JSON_PRETTY_PRINT);
                    }
        
                } else {
                    
                    echo json_encode("error_creating_account", JSON_PRETTY_PRINT);
                }
            }

        }

    } else {

        if ($pass==="") {
            
            echo json_encode("bad_password", JSON_PRETTY_PRINT);
    
        } else {

            $actdate=date('Y-m-d H:i:s');
            $sql="INSERT INTO users (username, password, mtx, status, date, ip, level, exp) VALUES ('$usr', '$pass', '500', 'normal', '$actdate', '$ip', '1', '1')";
            $result=mysqli_query($conn, $sql);
    
            if ($result==TRUE) {
                $tokn=generateToken($usr);
                $tkn=hash('sha256', $tokn);
                $tkn=hash('sha512', $tkn);

                $sql="INSERT INTO stat (top1, top10, top25, username, token) VALUES ('0', '0', '0', '$usr', '$tkn')";
                $result=mysqli_query($conn, $sql);
    
                if ($result==TRUE) {
                    $sql="UPDATE users SET token='$tkn' WHERE username='$usr' AND password='$pass'";
                    $result=mysqli_query($conn, $sql);
    
                    if ($result==TRUE) {
                        
                        $sql="INSERT INTO token (token, password) VALUES ('$tokn', '$pass')";
                        $result=mysqli_query($conn, $sql);
    
                        if ($result==TRUE) {
    
                            echo json_encode("$tokn", JSON_PRETTY_PRINT);
    
                        } else {
    
                            echo json_encode("error_creating_account_token_table", JSON_PRETTY_PRINT);
                        }
    
                    } else {
                        
                        echo json_encode("error_creating_account_stat", JSON_PRETTY_PRINT);
                    }
                } else {
                    
                    echo json_encode("error_creating_account_token", JSON_PRETTY_PRINT);
                }
    
            } else {
                
                echo json_encode("error_creating_account", JSON_PRETTY_PRINT);
            }
        }

    }

}

?>