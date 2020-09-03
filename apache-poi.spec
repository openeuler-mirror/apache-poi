%global reldate 20170915
Name:                apache-poi
Version:             3.17
Release:             1
Summary:             The Java API for Microsoft Documents
License:             ASL 2.0 and (CC-BY and CC-BY-SA and W3C) and GPLv3
URL:                 http://poi.apache.org/
Source0:             http://archive.apache.org/dist/poi/release/src/poi-src-3.17-20170915.tar.gz
# These two zip files renamed after download
#Source1: http://www.ecma-international.org/publications/files/ECMA-ST/Office%20Open%20XML%201st%20edition%20Part%204%20%28PDF%29.zip
#Source2: http://www.ecma-international.org/publications/files/ECMA-ST/Office%20Open%20XML%201st%20edition%20Part%202%20%28PDF%29.zip
Source1:             Office_Open_XML_1st_edition_Part_4__PDF_.zip
Source2:             Office_Open_XML_1st_edition_Part_2__PDF_.zip
Source3:             http://dublincore.org/schemas/xmls/qdc/2003/04/02/dc.xsd
Source4:             http://dublincore.org/schemas/xmls/qdc/2003/04/02/dcterms.xsd
Source5:             http://dublincore.org/schemas/xmls/qdc/2003/04/02/dcmitype.xsd
Source6:             http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd
Source7:             http://uri.etsi.org/01903/v1.3.2/XAdES.xsd
Source8:             http://uri.etsi.org/01903/v1.4.1/XAdESv141.xsd
Patch1:              apache-poi-3.14-compile-xsds.patch
Patch2:              apache-poi-3.14-build.patch
BuildArch:           noarch
BuildRequires:       jacoco javapackages-local jmh jmh-generator-annprocess
BuildRequires:       apache-commons-collections4 >= 4.1 apache-commons-codec apache-commons-logging
BuildRequires:       mvn(com.github.virtuald:curvesapi) mvn(dom4j:dom4j) mvn(junit:junit)
BuildRequires:       mvn(log4j:log4j:1.2.17) mvn(org.apache.ant:ant-junit)
BuildRequires:       mvn(org.apache.santuario:xmlsec) >= 2.0.1 mvn(org.apache.xmlbeans:xmlbeans)
BuildRequires:       mvn(org.bouncycastle:bcpkix-jdk15on) mvn(org.bouncycastle:bcprov-jdk15on)
BuildRequires:       mvn(org.hamcrest:hamcrest-core) mvn(org.ow2.asm:asm-all)
BuildRequires:       mvn(org.slf4j:slf4j-api) mvn(rhino:js)
BuildRequires:       fontconfig liberation-sans-fonts liberation-serif-fonts
%description
The Apache POI Project's mission is to create and maintain Java APIs for
manipulating various file formats based upon the Office Open XML standards
(OOXML) and Microsoft's OLE 2 Compound Document format (OLE2). In short, you
can read and write MS Excel files using Java. In addition, you can read and
write MS Word and MS PowerPoint files using Java. Apache POI is your Java
Excel solution (for Excel 97-2008). We have a complete API for porting other
OOXML and OLE2 formats and welcome others to participate.
OLE2 files include most Microsoft Office files such as XLS, DOC, and PPT as
well as MFC serialization API based file formats. The project provides APIs
for the OLE2 Filesystem (POIFS) and OLE2 Document Properties (HPSF).
Office OpenXML Format is the new standards based XML file format found in
Microsoft Office 2007 and 2008. This includes XLSX, DOCX and PPTX. The
project provides a low level API to support the Open Packaging Conventions
using openxml4j.
For each MS Office application there exists a component module that attempts
to provide a common high level Java API to both OLE2 and OOXML document
formats. This is most developed for Excel workbooks (SS=HSSF+XSSF). Work is
progressing for Word documents (HWPF+XWPF) and PowerPoint presentations
(HSLF+XSLF).
The project has recently added support for Outlook (HSMF). Microsoft opened
the specifications to this format in October 2007. We would welcome
contributions.
There are also projects for Visio (HDGF) and Publisher (HPBF).

%package javadoc
Summary:             Javadoc for %{name}
%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n poi-%{version}
%patch1
%patch2
find -name '*.class' -delete
find -name '*.jar' -delete
mkdir lib ooxml-lib
build-jar-repository -s -p lib \
  ant commons-collections4 commons-codec commons-logging bcprov bcpkix xmlsec slf4j/slf4j-api log4j-1.2.17 \
  junit hamcrest/core jmh/jmh-core jmh/jmh-generator-annprocess
build-jar-repository -s -p ooxml-lib dom4j xmlbeans/xbean curvesapi
pushd ooxml-lib
unzip "%SOURCE1" OfficeOpenXML-XMLSchema.zip
unzip "%SOURCE2" OpenPackagingConventions-XMLSchema.zip
cp -p %SOURCE3 .
cp -p %SOURCE4 .
cp -p %SOURCE5 .
cp -p %SOURCE6 .
cp -p %SOURCE7 .
cp -p %SOURCE8 .
popd
%pom_xpath_inject "pom:dependencies/pom:dependency[pom:artifactId ='ant']" \
  "<scope>provided</scope>" maven/poi-excelant.pom
for m in poi poi-excelant poi-examples poi-ooxml poi-ooxml-schemas poi-scratchpad ; do
%mvn_file org.apache.poi:${m} poi/apache-${m} poi/${m}
done
rm src/ooxml/testcases/org/apache/poi/xssf/usermodel/TestXSSFSheet.java \
 src/ooxml/testcases/org/apache/poi/xssf/usermodel/TestXSSFSheetMergeRegions.java
sed -i '/TestXSSFSheet/d' src/ooxml/testcases/org/apache/poi/xssf/usermodel/AllXSSFUsermodelTests.java
rm src/ooxml/testcases/org/apache/poi/sl/TestFonts.java
rm -f src/ooxml/testcases/org/apache/poi/xssf/streaming/TestAutoSizeColumnTracker.java
rm -f src/ooxml/testcases/org/apache/poi/xssf/streaming/TestSXSSFSheet.java
rm -f src/ooxml/testcases/org/apache/poi/poifs/crypt/TestSignatureInfo.java

%build
cat > build.properties <<'EOF'
main.ant.jar=lib/ant.jar
main.commons-collections4.jar=lib/commons-collections4.jar
main.commons-codec.jar=lib/commons-codec.jar
main.commons-logging.jar=lib/commons-logging.jar
main.log4j.jar=lib/log4j-1.2.17.jar
main.junit.jar=lib/junit.jar
main.jmh.jar=lib/jmh_jmh-core.jar
main.jmhAnnotation.jar=lib/jmh_jmh-generator-annprocess.jar
main.hamcrest.jar=lib/hamcrest_core.jar
ooxml.dom4j.jar=ooxml-lib/dom4j.jar
ooxml.curvesapi.jar=ooxml-lib/curvesapi.jar
ooxml.xmlbeans23.jar=ooxml-lib/xmlbeans_xbean.jar
ooxml.xmlbeans26.jar=ooxml-lib/xmlbeans_xbean.jar
dsig.xmlsec.jar=lib/xmlsec.jar
dsig.bouncycastle-prov.jar=lib/bcprov.jar
dsig.bouncycastle-pkix.jar=lib/bcpkix.jar
dsig.sl4j-api.jar=lib/slf4j_slf4j-api.jar
disconnected=1
DSTAMP=%{reldate}
EOF
export ANT_OPTS="-Xmx768m"
ant -propertyfile build.properties compile-ooxml-xsds jar maven-poms javadocs

%install
for m in poi poi-excelant poi-examples poi-ooxml poi-ooxml-schemas poi-scratchpad ; do
%mvn_artifact build/dist/maven/$m/${m}-%{version}.pom build/dist/maven/$m/${m}-%{version}.jar
done
%mvn_install -J build/tmp/site/build/site/apidocs

%files -f .mfiles
%doc KEYS
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Thu Aug 13 2020 chengzihan <chengzihan2@huawei.com> - 3.17-1
- Package init
