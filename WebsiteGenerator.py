import importlib
import os
import random
import shutil
import pathlib
import json


#def CreatePicture():
shutil.rmtree("Output")
shutil.copytree("OutputTemplate", "Output")
shutil.copytree("ProjectImages", "Output/Pictures/ProjectImages")
PageTemplate = open("PageTemplate.html", encoding="utf8").read()
ETRPageTemplate = open("EasyToReadTemplate.html", encoding="utf8").read()
ArticleTemplate = open("ArticleTemplate.html", encoding="utf8").read()
CoverTemplate = open("CoverTemplate.html", encoding="utf8").read()
ETRArticle = open("EasyToReadArticleTemplate.html", encoding="utf8").read()
ArticlesString = ""
ETRArticlesString = ""
ETRLeftTitles = ""
ETRRightTitles = ""
CoversString = '<div class="row">\n'
CoversCount = 0
OutputIndex = open("Output/index.html", 'w')
OutputETR = open("Output/accessible", 'w')
Articles = os.listdir("Articles")
for x in range(len(Articles)):
    if Articles[x][0] != 'X':
        if CoversCount == 4:
            CoversCount = 0
            CoversString += '\n</div>\n<div class="row">\n'
        ArticleMetadata = json.load( open("Articles/"+Articles[x]+"/Metadata.json", encoding="utf8"))
        metaTitle = ArticleMetadata["MetaTitle"]

        WorkingArticle = ArticleTemplate.replace("[Modal Body]", open("Articles/"+Articles[x]+"/Content.html", encoding="utf8").read())
        WorkingArticle = WorkingArticle.replace("[MetaTitle]", metaTitle)
        WorkingArticle = WorkingArticle.replace("[Title]", ArticleMetadata["Title"])

        WorkingCover = CoverTemplate.replace("[MetaTitle]", metaTitle)
        WorkingCover = WorkingCover.replace("[Cover]", "Pictures/Covers/"+metaTitle+"Cover.png")
        WorkingCover = WorkingCover.replace("[VideoGraphic]", "Pictures/VideoGraphics/"+metaTitle+"VideoGraphic.gif")

        WorkingETRArticle = ETRArticle.replace("[ModalBody]", open("Articles/"+Articles[x]+"/Content.html", encoding="utf8").read())
        WorkingETRArticle = WorkingETRArticle.replace("[Cover]", "Pictures/Covers/"+metaTitle+"Cover.png")
        WorkingETRArticle = WorkingETRArticle.replace("[VideoGraphic]", "Pictures/VideoGraphics/"+metaTitle+"VideoGraphic.gif")
        WorkingETRArticle = WorkingETRArticle.replace("[Title]", ArticleMetadata["Title"])
        WorkingETRArticle = WorkingETRArticle.replace("[MetaTitle]", metaTitle)
        
        WorkingETRTitle =  '<li><a href="#[MetaTitle]">[Title]</a></li>\n'.replace("[MetaTitle]", metaTitle)
        WorkingETRTitle =  WorkingETRTitle.replace("[Title]", ArticleMetadata["Title"])

        if CoversCount % 2:
            ETRLeftTitles += WorkingETRTitle
        else:
            ETRRightTitles += WorkingETRTitle

        CoversString += (WorkingCover + '\n')
        CoversCount+=1
        ArticlesString += WorkingArticle
        ETRArticlesString += WorkingETRArticle
        shutil.copy("Articles/"+Articles[x]+"/Cover.png", "Output/Pictures/Covers/"+metaTitle+"Cover.png")
        shutil.copy("Articles/"+Articles[x]+"/VideoGraphic.gif", "Output/Pictures/VideoGraphics/"+metaTitle+"VideoGraphic.gif")

CoversString += '</div>'

ETRPageTemplate = ETRPageTemplate.replace("[LeftTitles]",ETRLeftTitles)
ETRPageTemplate = ETRPageTemplate.replace("[RightTitles]",ETRRightTitles)
ETRPageTemplate = ETRPageTemplate.replace("[Articles]",ETRArticlesString)

PageTemplate = PageTemplate.replace("[Cover]", CoversString)
PageTemplate = PageTemplate.replace("[Articles]", ArticlesString)
OutputIndex.write(PageTemplate)
OutputIndex.close()
OutputETR.write(ETRPageTemplate)
OutputETR.close()