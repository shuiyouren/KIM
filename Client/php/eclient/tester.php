<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:fb="http://www.facebook.com/2008/fbml"> 
<head>
<title>EServer- Tester</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />

</head>
<body>


<pre>
<xmp>

<root>
<erequests>
  <erequest type="messenger" id="0">
  <body>
   <subtype>message</subtype>
   <text>Hello World!</text>
   <format></format>
  </body>
  </erequest>
 </erequests>
</root>

<root>
<erequests>
  <erequest type="check_listen" id="0">
  <body></body>
  </erequest>
 </erequests>
</root>

</xmp>
</pre>

<form action="index-sample.php" method="post">
<p>
<textarea rows="10" cols="100" name="erequest"></textarea>
</p>
<p>
<input type="submit" name="enviar" value="Enviar" />
</p>
</form>

</body>
</html>
