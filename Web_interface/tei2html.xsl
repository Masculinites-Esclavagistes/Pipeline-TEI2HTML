<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  version="2.0">
  
  <xsl:output method="html" encoding="UTF-8" indent="yes"/>
  <xsl:strip-space elements="*"/>
  
  <!-- MAIN TEMPLATE -->
  <xsl:template match="/">
    <html>
      <head>
        <title>
          <xsl:value-of select="//tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/>
        </title>
        <style>
          body { 
          font-family: "Optima", sans-serif; 
          display: flex; 
          margin: 0; 
          height: 100vh; 
          overflow: hidden; 
          }
          nav { 
          width: 20%; 
          padding: 10px; 
          background-color: #e7d9cb; 
          height: 100vh; 
          overflow-y: auto; 
          position: sticky; 
          top: 0; 
          line-height: 1.4;
          }
          main { 
          width: 80%; 
          padding: 10px; 
          height: 100vh; 
          overflow-y: auto; 
          }
          .pb-block { 
          display: flex; 
          gap: 20px; 
          margin-bottom: 40px; 
          }
          .pb-block img { 
          max-height: 600px; 
          cursor: zoom-in;
          border: 1px solid #e7d9cb; 
          box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
          }
          .transcription p { 
          white-space: pre-wrap; 
          line-height: 1.0;
          }
          h1, h2, h3 { 
          margin-top: 2em; 
          }
          h2  { 
          color: #ca4c49; 
          }
          h3  { 
          font-size: 14px;
          }
          #credits {
          margin-top: 100px;
          font-size: 0.9em;
          color: #555;
          background-color: #f4ede7;
          }
        </style>
      </head>
      <body>
        
        <!-- NAVIGATION -->
        <nav>
          <h3>Navigation</h3>
          <ul>
            <xsl:for-each select="//tei:div[@type='file']">
              <li>
                <a href="#{generate-id()}">
                  <xsl:value-of select="replace(@corresp, '_', ', ')"/>
                </a>
              </li>
            </xsl:for-each>
          </ul>
        </nav>
        
        <!-- MAIN CONTENT -->
        <main>
          <h1><xsl:value-of select="//tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/></h1>
          
          <xsl:for-each select="//tei:div[@type='file']">
            <div class="file-section" id="{generate-id()}">
              <h2>
                <xsl:value-of select="replace(@corresp, '_', ', ')"/>
              </h2>
              <xsl:for-each select="tei:pb">
                <xsl:variable name="corresp" select="@corresp"/>
                <xsl:variable name="folder" select="substring-before($corresp, '/')"/>
                <xsl:variable name="imgfile" select="substring-after($corresp, '/')"/>
                <xsl:variable name="imgpathJPG" select="concat('data/', $folder, '/', $imgfile, '.JPG')"/>
                <xsl:variable name="imgpathJPG" select="concat('file:/Users/philipm/Documents/Pipeline_TEI/PYTHON/data/', $folder, '/', $imgfile, '.JPG')" />
                <xsl:variable name="imgpathjpg" select="concat('file:/Users/philipm/Documents/Pipeline_TEI/PYTHON/data/', $folder, '/', $imgfile, '.jpg')" />
                <!--<xsl:variable name="imgpathjpg" select="concat('data/', $folder, '/', $imgfile, '.jpg')"/>-->
                
                <div class="pb-block">
                  <div class="transcription">
                    <p>
                      <strong>
                        <xsl:value-of select="replace($folder, '_', ', ')"/>
                        <xsl:text> - </xsl:text>
                        <xsl:value-of select="$imgfile"/>
                      </strong>
                      <br/>
                      <!-- Capture all following siblings up to next pb -->
                      <xsl:for-each select="following-sibling::*[not(self::tei:pb)][generate-id(preceding-sibling::tei:pb[1]) = generate-id(current())]">
                        <xsl:apply-templates select="."/>
                      </xsl:for-each>
                    </p>
                  </div>
                  <div>
                    <a href="{$imgpathjpg}" target="_blank">
                      <img src="{$imgpathjpg}" alt="{$imgfile}"/>
                    </a>
                  </div>
                </div>
              </xsl:for-each>
            </div>
          </xsl:for-each>
          
          <!-- CREDITS -->
          <div id="credits">
            <p><strong>Terms of Use and Citation</strong><br/>
              The citation terms are as follows:
              "MEGV Corpus: Selection of personnel files of colonial agents (COL E), Secrétariat d'Etat à la Marine, ANOM. SNF (n°219753), University of Geneva, dir. Marie Houllemare, [date of consultation]".
            </p>
            <p>
              Original code &amp; design, data processing:
              <a href="mailto:marion.philip@unige.ch">marion.philip@unige.ch</a>
            </p>
          </div>
        </main>
      </body>
    </html>
  </xsl:template>
  
  <!-- HANDLE lb TAGS -->
  <xsl:template match="tei:lb">
    <br/>
  </xsl:template>
  
  <!-- DEFAULT TEMPLATE -->
  <xsl:template match="tei:*">
    <xsl:copy>
      <xsl:apply-templates select="@* | node()"/>
    </xsl:copy>
  </xsl:template>
  
  <xsl:template match="@*">
    <xsl:copy/>
  </xsl:template>
</xsl:stylesheet>
