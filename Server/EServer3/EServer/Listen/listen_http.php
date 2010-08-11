<?php

require_once ( "listen_http/EData.php" ) ;
require_once ( "listen_http/ERequest.php" ) ;

class ListenHTTP
{

    private $onListen ;
    public $listenData ;
    private $EServer ;

    //public $Requests ;

    public function registerOnListen( &$EServer, $onListenName ){
        $this->EServer = &$EServer ;
        $this->onListen = $onListenName ;
        //echo "function: ".$onListenName ;
        //echo $this->onListen ;

        // Name->"name", function->function
        $this->ProcessRequests = $this->Process->ProcessTokens ;
    }

    public function Inject( $input ){


                /*
                //$url = "http://www.mercadolibre.com.mx/jm/searchXml?as_nickname=los%20g%C3%BCeros&as_categ_id=3390&noQCat=Y8&user=EIBRIEL84&pwd=RUlCUklFTDg0RUlCUklFTDhuNA%3D%3D" ;
				curl_setopt($ch, CURLOPT_URL, $url );
				curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
				$output = curl_exec($ch);

				$error_xml = false ;

				if( curl_errno($ch) )
				{
					$error_xml = true ;
					//DEBUG
					if ( $this->debug) echo "ERROR CURL ( ".$url.") : ".curl_error ($ch)."<br />" ;
				}

				try {
					if ( !$error_xml ) $xml_items = new SimpleXMLElement($output);
				} catch (Exception $e) {
					$error_xml = true ;
					//DEBUG
					if ( $this->debug) echo "ERROR XML ( ".$url."): ".$e."<br />XML: ".$output."<br />" ;
				}

				curl_close($ch);

				if ( isset ( $xml_items->listing->items->item[0]['id'] ) && !$error_xml ) {

					$items_array = (array) $xml_items->listing->items ;

					if ( !isset ($items_array['item']['id']) ) $items_array = $items_array['item'] ;
					
					foreach ( $items_array as $item ) {

						$titulo = (string) $item->title ;
						$link = (string) $item->link;
						$imagen_url = (string) $item->image_url ;
						$id = (string) $item['id'] ;
						$items[] = Array ( 'id' => $id, 'titulo' => $titulo, 'link' => $link, 'image_url' => $imagenurl ) ;

						$link = str_replace ( 'XXX', $this->herramienta, $link ) ;

						$titulo_sql = mysql_real_escape_string( $titulo ) ;
						$link_sql = mysql_real_escape_string( $link ) ;
						$imagen_url_sql = mysql_real_escape_string( $imagen_url ) ;
						$id_sql = mysql_real_escape_string( $id ) ;
						$user_id_sql = mysql_real_escape_string( $user_id ) ;

						//Inserta nuevos Articulos
						if ( !isset ( $this->articulos_usuario[ $id ] ) ) {
							$consulta = "INSERT INTO $Ltable VALUES( '$id_sql', '$user_id_sql', '$link_sql', '$titulo_sql', '$imagen_url_sql', '1', '0', '0' )" ;
							$resultado = mysql_query( $consulta ) or die ( '<br />La consulta Insert fall&oacute;: ' . mysql_error() ) ;
							$publicado = 1 ;
							$vendido = 0 ;
							$nuevo = 1 ;
					
							$this->nuevos_arr[] = Array ( "titulo" => $titulo, "link" => $link, "imagen_url" => $imagen_url ) ;

							$this->articulos_usuario[ $id ][ 'existe' ] = true ;

							//DEBUG
							if ( $this->debug) echo '<p><b>Inserta02</b> '.$id.' '.$this->articulos_usuario[ $id ][ 'titulo' ].' '. $this->articulos_usuario[ $id ][ 'existe' ] .'</p>' ;

							$this->articulos_nuevos++;
						} else {

							$publicado = $this->articulos_usuario[ $id ][ 'publicado' ] ;
							$vendido = $this->articulos_usuario[ $id ][ 'vendido' ] ;
							$oculto = (integer) $this->articulos_usuario[ $id ][ 'oculto' ] ;

							$this->articulos_usuario[ $id ][ 'existe' ] = true ;

							//DEBUG
							//if ( $this->debug ) echo '<p> Nada 03 '.$id.' '.$this->articulos_usuario[ $id ][ 'titulo' ].' '. $this->articulos_usuario[ $id ][ 'existe' ] .'</p>' ;

							$nuevo = 0 ;
						}

						if ( !$oculto ) {
                            $titulo = addslashes( $titulo ) ;
							$this->respuesta .= " articulos [".$numero."] = new Articulo (".$id.", '".$titulo."', '".$link."', '".$imagen_url."', ".$publicado.", ".$vendido.", ".$nuevo." ) ;" ;
                            //$this->respuesta .= "\n" ;
						}

						$numero++ ;

					} //foreach ( $items_array as $item ) {
				}//if ( isset ( $xml_items->listing->items->item[0]['id'] ) ) {
			}//foreach ( $xml->categories->category as $categoria ) {
        */

        //echo "inject\n" ;

        $error_xml = false ;
        $Requests = array () ;

        try {
			$xml_requests = new SimpleXMLElement( stripslashes ($input) );
		} catch (Exception $e) {
			$error_xml = true ;
			//DEBUG
			echo "ERROR XML ( ".$url."): ".$e."<br />XML: ".$input."<br />" ;
		}

        if ( isset ( $xml_requests->erequests ) && !$error_xml ) {
            $requests_array = (array) $xml_requests->erequests ;

            foreach ( $requests_array as $request ) {
                $req = new ERequest ( (string) $request['type'], $request->body->asXML() ) ;
                $Requests[] = $req ;
               // echo $request['name'] ;
            }

        }

        $this->listenData = new EData ( $Requests, "") ;

        //$this->listenData = $this->Requests ;
        $func = $this->onListen ;
        $this->EServer->$func ( $this->listenData ) ;
    }

}
