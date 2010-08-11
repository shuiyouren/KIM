<?php
require_once('db_mysql/sql_connect.php');

class DBMysql 
{

    private $tablePrefix = "" ;
    public $error = "" ;

	public function __construct ( ) {
        //$this->tables['users'] = 'es_users' ;
	}

    public function install () {
    }

    public function setTablePrefix ( $tablePrefix_ ) {
        $this->tablePrefix = $tablePrefix_ ;
        //echo $this->tablePrefix.":" ;
    }

    public function update ( $table_, $fields, $where, $limit=false ) {

        //$table = $this->tables [ $table_ ] ;
        $table = $this->tablePrefix."".$table_ ;

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

		//echo " <!-- Request: $request -->\n" ;

        return $resultado = mysql_query($request) ;
        //return $this->toArray ($request) ;
    }

    public function select ( $table_, $fields=false, $where=false, $limit=false ) {

        //$table = $this->tables [ $table_ ] ;
//echo $this->tablePrefix ;
        $table = $this->tablePrefix."".$table_ ;
//echo $table ;
        $request = "SELECT " ;

		if ($fields == false ) {
			$request .= "*" ;
		} else {
			$num = 0 ;
			foreach ( $fields as $field ) {
				if ( $num>0 ) $request.=", " ;
				$request .= "`".$field."`" ;
				$num++ ;
			}
		}

        $request .= " FROM `$table` " ;
		
		if ($where) {
		
			$request .= " WHERE " ;
			$num = 0 ;

			foreach ( $where as $we ) {
				if ( $num>0 ) $consulta.=", " ;
				$request .= "`".$we[0]."`='".$we[1]."'" ;
				$num++ ;
			}
		}

        if ($limit) $request .= " LIMIT $limit ;" ;

		//echo " <!-- Request: $request -->\n" ;

        return $this->toArray ($request) ;
    }

    function insert ( $table_, $fields ) {
        //$table = $this->tables [ $table_ ] ;
        $table = $this->tablePrefix."".$table_ ;

        $request = "INSERT INTO `$table` SET " ;
        $num = 0 ;
        foreach ( $fields as $field ) {
            if ( $num>0 ) $request.=", " ;
            $request .= "`".$field[0]."`='".$field[1]."'" ;
            $num++ ;
        }

        $request .= ";" ;

		//echo " <!-- Request: $request -->\n" ;

        return $resultado = mysql_query($request) ;
    }

    function toArray ( $request ) {
        $result = mysql_query($request) ;

        if ( $result == false ) {
            $this->error = mysql_error() ;
            return false ;
        }

        //print_r ( $request ) ;

        /*
        while ($row = mysql_fetch_object($result)) {
           $AResult[] = $row ;
        }
        */
        while ( $row = mysql_fetch_array($result, MYSQL_ASSOC) ) {
            $AResult[] = $row ;
        }

        return $AResult ;
    }

}

?>
