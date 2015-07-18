# L2FrenchWritingAnalyser
analyses French L2 writing

subdirectories:

preAnalysis:
  functions for running MElt, FRMG etc. over the corpus
  
textExtractor:
  calculates all the relevant variables
  
compareCorpus:
  analysis of the FipsOrtho corpus

postAnalysis:
  functions for analysing the resulting data (currently we don't use this, weka instead)
  
otherAnalysis:
  alternative tools to the text Extractor but using the same information
  
preTreatment:
  pre treatments specific to the corpora used
  
spellCorrect:
  a tentative at a spelling corrector (following Peter Norvig's example), not currently used
  
testExternalModules:
  files for testing if external modules work / are usable
  
oldCode:
  older scripts that may or may not still work (needs review)
