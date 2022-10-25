<?php

function addServ($srv_ip, $srv_port, $class) {

    global $conn;
    
    if ($class=="normal") {
        $sql="SELECT server_port FROM servers WHERE server_ip='$srv_ip'";
        $result=mysqli_query($conn, $sql);
    
        if (mysqli_num_rows($result)!=0) {
    
            echo json_encode("already_reg", JSON_PRETTY_PRINT);
    
        } else {
            $sql="SELECT bullet_server_ip FROM servers WHERE server_ip='0'";
            $result=mysqli_query($conn, $sql);

            if (mysqli_num_rows($result)!=0) {
                $srv=mysqli_fetch_assoc($result)['bullet_server_ip'];
                $sql="UPDATE servers SET server_ip='$srv_ip', server_port='$srv_port' WHERE bullet_server_ip='$srv'";
                $result=mysqli_query($conn, $sql);

                if ($result==TRUE) {

                    echo json_encode("ok", JSON_PRETTY_PRINT);

                } else {
        
                    echo json_encode("error", JSON_PRETTY_PRINT);
        
                }

            } else {
                $sql="INSERT INTO servers (server_ip, server_port, bullet_server_ip, bullet_server_port) VALUES ('$srv_ip', '$srv_port', '0', '0')";
                $result=mysqli_query($conn, $sql);
        
                if ($result==TRUE) {
        
                    echo json_encode("ok", JSON_PRETTY_PRINT);
        
                } else {
        
                    echo json_encode("error", JSON_PRETTY_PRINT);
        
                }

            }
    
        }
    
    } else if ($class=="bullet") {
        $sql="SELECT server_port FROM servers WHERE bullet_server_ip='$srv_ip'";
        $result=mysqli_query($conn, $sql);
    
        if (mysqli_num_rows($result)!=0) {
    
            echo json_encode("already_reg", JSON_PRETTY_PRINT);
    
        } else {
            $sql="SELECT server_ip FROM servers WHERE bullet_server_ip='0'";
            $result=mysqli_query($conn, $sql);

            if (mysqli_num_rows($result)!=0) {
                $srv=mysqli_fetch_assoc($result)['server_ip'];
                $sql="UPDATE servers SET bullet_server_ip='$srv_ip', bullet_server_port='$srv_port' WHERE server_ip='$srv'";
                $result=mysqli_query($conn, $sql);

                if ($result===TRUE) {

                    echo json_encode("ok", JSON_PRETTY_PRINT);

                } else {
        
                    echo json_encode("error", JSON_PRETTY_PRINT);
        
                }

            } else {
                $sql="INSERT INTO servers (bullet_server_ip, bullet_server_port, server_ip, server_port) VALUES ('$srv_ip', '$srv_port', '0', '0')";
                $result=mysqli_query($conn, $sql);
        
                if ($result==TRUE) {
        
                    echo json_encode("ok", JSON_PRETTY_PRINT);
        
                } else {
        
                    echo json_encode("error", JSON_PRETTY_PRINT);
        
                }

            }
    
        }
    
    }
    
    }

?>