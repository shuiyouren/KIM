<?php

$port = 1864 ;
$timeout = 10 ;
$errno = -1 ;
$errstr = '' ;
$ip=$_SERVER['REMOTE_ADDR'] ;
#$ip = "127.0.0.1"

if (0) {


	$portsopen =  @fsockopen("$ip", $port, $errno, $errstr, $timeout);

	echo $ip ;
	if ($portsopen) {
		echo "open" ;
	} else {
		echo " - close - ".$errstr ;
	}

} elseif (0) {

	#$sock = socket_create(AF_INET, SOCK_STREAM, SOL_TCP) ;

	#$portsopen = 1 ;


	try {
		$sock = @stream_socket_client("udp://$ip:$port", $errno, $errstr, $timeout);
        #$sock = @stream_socket_client("udp://stun.ekiga.net:3478", $errno, $errstr, $timeout);
        #$sock = @stream_socket_client("udp://stun.xten.com:3478", $errno, $errstr, $timeout);
	} catch (Exception $e) {
		echo "Error: ".$errstr ;
	}

    if (!$sock) {
        echo "ERROR: $errno - $errstr<br />\n";
    } else {
        echo "Enviando Hola a $ip:$port" ;
        fwrite($sock, "Hola\n");
        #echo fread($sock, 26);
        #fclose($sock);
    }

/*
	if (!$sock) {
		 echo "$errstr ($errno)<br />\n";
	} else {
		echo "anda." ;
		fwrite($sock, "Say Hello Word");
		while (!feof($sock)) {
			echo fgets($sock, 1024);
		}
		fclose($sock);
	}
*/
} else {

	#$sock = socket_create(AF_INET, SOCK_STREAM, SOL_TCP) ;
    $sock = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP) ;
	$portsopen = socket_connect ( $sock, $ip, $port ) ;
	socket_write ( $sock, 'Hola_Ei' ) ;
	socket_close ( $sock ) ;


}

?>
