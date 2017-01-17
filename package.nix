{ stdenv, fetchurl }:

stdenv.mkDerivation rec {

  version = "";
  name = "";
  
  src = fetchurl {
    url = "";
    sha256 = "";
  };

  builder = builtins.toFile "builder.sh" "
    
    ";

  meta = {
    description = "";
    longDescription = '' '';
    homepage = "";
    license = stdenv.lib.licenses.gpl2;
    platforms = stdenv.lib.platforms.linux;
  };

}
