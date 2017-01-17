{ stdenv, fetchurl }:

stdenv.mkDerivation rec {

  version = "";
  name = "";
  
  src = fetchurl {
    url = "";
    sha256 = "";
  };

  builder = builtins.toFile "builder.sh" "
    source $stdenv/setup

    mkdir -p $out
    ";

  meta = {
    description = "";
    longDescription = '' '';
    homepage = "";
    license = stdenv.lib.licenses.gpl2;
    platforms = stdenv.lib.platforms.all;
  };

}
