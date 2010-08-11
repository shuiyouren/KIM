<?php
require_once('sql_connect.php');

class store 
{

	function __construct () {
        $this->tables['users'] = 'es_users' ;
	}

    public function update ( $table_, $fields, $where, $limit=false ) {

        $table = $this->tables [ $table_ ] ;

        $request = "UPDATE `$table` SET " ;

        $num = 0 ;
        foreach ( $fields as $field ) {
            if ( $num>0 ) $request.=", " ;
            $request .= "`".$field[0]."`='".$field[1]."'" ;
            $num++ ;
        }
        $request .= " WHERE " ;
        $num = 0 ;

        foreach ( $where as $we ) {
            if ( $num>0 ) $consulta.=", " ;
            $request .= "`".$we[0]."`='".$we[1]."'" ;
            $num++ ;
        }

        if ($limit) $request .= " LIMIT $limit ;" ;

		echo " <!-- Request: $request -->\n" ;

        return mysql_query($request) ;
    }

    public function select ( $table_, $fields, $where, $limit=false ) {

        $table = $this->tables [ $table_ ] ;

        $request = "SELECT " ;

        $num = 0 ;
        foreach ( $fields as $field ) {
            if ( $num>0 ) $request.=", " ;
            $request .= "`".$field."`" ;
            $num++ ;
        }

        $request .= " FROM `$table` " ;

        $request .= " WHERE " ;
        $num = 0 ;

        foreach ( $where as $we ) {
            if ( $num>0 ) $consulta.=", " ;
            $request .= "`".$we[0]."`='".$we[1]."'" ;
            $num++ ;
        }

        if ($limit) $request .= " LIMIT $limit ;" ;

		echo " <!-- Request: $request -->\n" ;

        return mysql_query($request) ;
    }

    function insert ( $table_, $fields ) {
        $table = $this->tables [ $table_ ] ;

        $request = "INSERT INTO `$table` SET " ;
        $num = 0 ;
        foreach ( $fields as $field ) {
            if ( $num>0 ) $request.=", " ;
            $request .= "`".$field[0]."`='".$field[1]."'" ;
            $num++ ;
        }

        $request .= ";" ;

		echo " <!-- Request: $request -->\n" ;

        return $resultado = mysql_query($request) ;
    }

}

?>
