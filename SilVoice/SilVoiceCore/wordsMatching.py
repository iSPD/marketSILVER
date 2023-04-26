from jamo import h2j, j2hcj
import difflib
import random
from sentence_preprocessing import sentence_preprocessing
from goSilverMarketP import goSilverKiwi, goSilverKiwiForSum

# def print(a):
#     a = None

def diff(word1, word2):
    '''두 유니코드 단어의 거리를 계산하여 차이를 반환한다'''
    # L1 = ''.join(reduce(lambda x1,x2: x1+x2, map(segment, word1)))
    # L2 = ''.join(reduce(lambda x1,x2: x1+x2, map(segment, word2)))
    L1 = j2hcj(h2j(word1))
    L2 = j2hcj(h2j(word2))
    
    # print(f'{L1}, {L2}')
    differ = difflib.SequenceMatcher(None, L1, L2)
    return differ.ratio()
# print(segment(u'ㅜ'))

# print(diff('삼겹살', '금겹살'), diff('삼겹살', '오겹살'), diff('삼겹살', '초콜릿'), diff('삼겹살', '살'))

def wordMatching(word1, word2):
    
    # 햄버거, 햄버거
    print(f'wordMatching : {word1}, {word2}')
    
    googleSplit = word1.split(' ')
    ourSplit = word2.split(' ')
    
    # googleSplit = word1
    # ourSplit = word2
        
    resultList = []
    failList = []
    
    for partial1 in googleSplit:
        print(f'partial1 : {partial1}')
        maxScore = 0.0
        selectedName = ''
        for partial2 in ourSplit:
            # print(f'length {len(partial1)}, {len(partial2)}')
            if len(partial1) > len(partial2):
                addLength = len(partial1) - len(partial2)
                for i in range(0, addLength):
                    if '폏' in partial1:
                        partial2 += '캭'
                    else:
                        partial2 += '폏'
            elif len(partial2) > len(partial1):
                addLength = len(partial2) - len(partial1)
                for i in range(0, addLength):
                    if '폏' in partial2:
                        partial1 += '캭'
                    else:
                        partial1 += '폏'
                    
            # print(f'{partial1}, {partial2}')
                
            currentScore = diff(partial1, partial2)
            # print(f'{partial1} vs {partial2} = {currentScore}')
            if currentScore > maxScore:
                maxScore = currentScore
                selectedName = partial2
                
            partial1 = partial1.replace('캭', '').replace('폏', '')
        
        # partial1 = partial1.replace('캭', '').replace('폏', '')
        selectedName = selectedName.replace('캭', '').replace('폏', '')
        
        # print(f'You WIN! {partial1} vs {selectedName} = {maxScore}\n\n')
        if maxScore > 0.7:
            resultList.append([partial1, selectedName, maxScore])
        else:
            failList.append([partial1, selectedName, maxScore])
        
    # print(f'짝궁성공 : {resultList}')
    # print(f'매칭성공했으나 70프로 미만인 친구들 : {failList}')
    
    # print('\n형태소 분석 시작')
    totalResult = []
    for result in resultList:
        # print(f'result : {result}')
        # keyword1, length1 = sentence_preprocessing(result[0])
        # keyword2, length2 = sentence_preprocessing(result[1])

        # keyword1 = goSilverKiwi(result[0])
        # keyword2 = goSilverKiwi(result[1])
        
        # print(f'짝궁 성공한 친구들 형태소 돌렸을때 : keyword1 : {keyword1}, keyword2 : {keyword2}')
        # if len(keyword1) != 0 and len(keyword2) != 0:
        #     totalResult.append([keyword1[0], keyword2[0]])
        # print('\n\n')
        
        # print(result[0])
        # print(result[1])
        totalResult.append([result[0], result[1]])
        
    return totalResult

def makeCompareWord(inSentence):
    words = inSentence.split(' ')
    wordsLength = len(words)
    
    totalWords = []
    for i in range(wordsLength):
        totalWords.append(words[i])
        if i != (wordsLength-1):
            totalWords.append(words[i]+ '' + words[i+1])
    
    # # 5개로 따지면...
    # totalWords = []
    # for i in range(0, wordsLength):
    #     if i == 0:
    #         for j in range(0, wordsLength):
    #             temp = words[j]
    #             totalWords.append(temp)
    #     elif i == 1:
    #         # temp = words[0] + words[1]
    #         # temp = words[1] + words[2]
    #         # temp = words[2] + words[3]
    #         # temp = words[3] + words[4]
    #         for j in range(0, wordsLength-1):
    #             temp = words[j] + '' + words[j+1]
    #             totalWords.append(temp)
    #     # elif i == 2:
    #     #     # temp = words[0] + words[1] + words[2]
    #     #     # temp = words[1] + words[2] + words[3]
    #     #     # temp = words[2] + words[3] + words[4]
            
    #     #     for j in range(0, wordsLength-2):
    #     #         temp = words[j] + words[j+1] + words[j+2]
    #     #         totalWords.append(temp)
    #     # elif i == 3:
    #     #     # temp = words[0] + words[1] + words[2] + words[3]
    #     #     # temp = words[1] + words[2] + words[3] + words[4]
            
    #     #     for j in range(0, wordsLength-3):
    #     #         temp = words[j] + words[j+1] + words[j+2] + words[j+3]
    #     #         totalWords.append(temp)
    #     # elif i == 4:
    #     #     # temp = words[0] + words[1] + words[2] + words[3] + words[4]
            
    #     #     for j in range(0, wordsLength-4):
    #     #         temp = words[j] + words[j+1] + words[j+2] + words[j+3] + words[j+4]
    #     #         totalWords.append(temp)
    #     # elif i == 5:
    #     #     for j in range(0, wordsLength-5):
    #     #         temp = words[j] + words[j+1] + words[j+2] + words[j+3] + words[j+4] + words[j+5]
    #     #         totalWords.append(temp)

    return totalWords

def cleanList(inputList):
    delList = []
    for index1 in range(0, len(inputList)):
        for index2 in range(0, len(inputList)):
            if(index2 == index1): continue
            
            if index2+1 !=  index1 and index2 < index1:
                sumWord = inputList[index2][0] + inputList[index2+1][0]
                if(sumWord == inputList[index1][0]):
                    # print(f'inputList[index2][0] : {inputList[index2][0]}, inputList[index2+1][0] : {inputList[index2+1][0]}')
                    # print(sumWord)
                    delList.append(inputList[index2])
                    delList.append(inputList[index2+1])
                                                
    for delete in delList:
        # print(f'delete : {delete}')
        try:
            inputList.remove(delete)
        except Exception as e:
            print(e)
        
    return inputList

def cleanList2(inputList):
    delList = []
    for index1 in range(0, len(inputList)):
        for index2 in range(0, len(inputList)):
            if(index2 == index1): continue
            
            if inputList[index2][0] in inputList[index1][0]:
                # print(inputList[index2])
                delList.append(inputList[index2])
                            
    for delete in delList:
        try:
            inputList.remove(delete)
        except Exception as e:
            print(e)
        
    return inputList

def doKiwi(inputList):
    totalResult = []
    for result in inputList:
        # print(f'result : {result}')
        # keyword1, length1 = sentence_preprocessing(result[0])
        # keyword2, length2 = sentence_preprocessing(result[1])

        keyword1, whereIndex1 = goSilverKiwi(result[0])
        keyword2, whereIndex2 = goSilverKiwi(result[1])
        
        # print(f'짝궁 성공한 친구들 형태소 돌렸을때 : keyword1 : {keyword1}, keyword2 : {keyword2}')
        # print(f'{len(keyword1)}, {len(keyword2)}')
        # if len(keyword1) != 0 and len(keyword2) != 0:
        #     for index in range(0, len(keyword1)):
        #         totalResult.append([keyword1[index], keyword2[index]])
        
        print(f'keyword1 : {keyword1}, keyword2 : {keyword2}')
        print(f'whereIndex1 : {whereIndex1}, whereIndex2 : {whereIndex2}')
        print(f'{len(keyword1)}, {len(keyword2)}')
                
        # if len(keyword1) != 0 and len(keyword2) == 0:
        if len(keyword1) != 0 and len(keyword2) == 0:    
            for index in range(0, len(keyword1)):
                copyIndexWord = ''
                for wIndex in whereIndex1:
                    start = wIndex[0]
                    length = wIndex[1]
                    copyIndexWord += result[1][start:start+length]
                
                totalResult.append([keyword1[index], copyIndexWord])
        elif len(keyword1) == 0 and len(keyword2) != 0:
            for index in range(0, len(keyword2)):
                copyIndexWord = ''
                for wIndex in whereIndex2:
                    start = wIndex[0]
                    length = wIndex[1]
                    copyIndexWord += result[0][start:start+length]
                
                totalResult.append([copyIndexWord, keyword2[index]])
        else: #두개 길이가 다르면 에러나겠지 
            for index in range(0, len(keyword1)):
                if len(keyword1[index]) < len(keyword2[index]):
                    copyIndexWord = ''
                    for wIndex in whereIndex2:
                        start = wIndex[0]
                        length = wIndex[1]
                        copyIndexWord += result[0][start:start+length]
                    totalResult.append([copyIndexWord, keyword2[index]])
                elif len(keyword1[index]) > len(keyword2[index]):
                    copyIndexWord = ''
                    for wIndex in whereIndex1:
                        start = wIndex[0]
                        length = wIndex[1]
                        copyIndexWord += result[1][start:start+length]
                    totalResult.append([keyword1[index], copyIndexWord])
                else:
                    totalResult.append([keyword1[index], keyword2[index]])
        
    return totalResult

def removeSame(inputList):
    # totalResult2 = set([tuple(set(item)) for item in totalResult])
    totalResult = []
    for item in inputList:
        doAdd = True
        for item2 in totalResult:
            if item == item2:
                doAdd = False 
            
        # print(doAdd)
        if doAdd == True:    
            totalResult.append(item)
    
    return totalResult
    
def checkSpell(inputList):
    from hanspell import spell_checker 
    def spell_check(sentence):
        sent = sentence
        spelled_sentence = spell_checker.check(sent)
        # print(f"Raw Sent : {sent}")

        hanspell_sentence = spelled_sentence.checked
        # print(f"Checked Sent : {hanspell_sentence}")

        return hanspell_sentence
        # return sentence
        
    # 스펠링 체크해서 띄어쓰기 보정 
    totalResult = []    
    for result in inputList:
        # print(f'result : {result}')
        # keyword1, length1 = sentence_preprocessing(result[0])
        # keyword2, length2 = sentence_preprocessing(result[1])

        keyword1 = spell_check(result[0])
        keyword2 = spell_check(result[1])
        
        totalResult.append([keyword1, keyword2])
        # print('\n\n')   
        
    return totalResult
    
def sumWords(inputWord1, inputWord2):
    # print('start->>>>>>>>>>>>>>>>>')    
    indexList1 = []
    indexList2 = []
    
    for index1, ch1 in enumerate(inputWord1):
        # print(ch1)
        for index2, ch2 in enumerate(inputWord2):
            if ch1 == ch2 and ch1 != ' ':
                # print(f'ch1 : {ch1} ch2 : {ch2} index : {index1}, index : {index2}')
                indexList1.append(index1)
                indexList2.append(index2)
                
    # print(indexList1)
    # print(indexList2) 
   
    isLine = False
    sameWord = ''
    newList1 = []
    newList2 = []
    for index in range(len(indexList1)-1):
        if (indexList1[index] + 1) == indexList1[index+1]:
            sameWord += inputWord1[indexList1[index]]
            newList1.append(indexList1[index])
            newList2.append(indexList2[index])
            
            if (index + 1) == len(indexList1) - 1:
                sameWord += inputWord1[indexList1[index+1]]
                newList1.append(indexList1[index+1])
                newList2.append(indexList2[index+1])
        else:
            if (indexList1[index] - 1) == indexList1[index-1]:
                sameWord += inputWord1[indexList1[index]]
                newList1.append(indexList1[index])
                newList2.append(indexList2[index])
            
    # print(f'sameWord : {sameWord}')

    if sameWord != '':
        isLine = True
          
    # print(newList1)
    # print(newList2)  
    if isLine == True and newList1[-1] == (len(inputWord1) - 1) and newList2[0] == 0:
        # print(f'sameWord : {sameWord}')
        word1 = inputWord1.replace(sameWord, '')
        word2 = inputWord2
        sumWord = word1 + word2
        
        # print(f'sumWord : {sumWord}')
        return True, sumWord
    elif inputWord1[-1] == inputWord2[0]:
        word1 = inputWord1.replace(inputWord1[-1], '')
        word2 = inputWord2
        sumWord = word1 + word2
        
        # print(f'sumWord : {sumWord}')
        return True, sumWord
    else:
        return False, ""
    
def sumWordsAll(wordList):
    # wordList = [['카레용 돼지고기', '카레용 돼지고기'], ['돼지고기 부위', '돼지고기 부위'], ['부위 사고 싶다', '부위 자고 싶어'], ['싶다 갱갱갱', '싶어 뱅뱅뱅']]
    # wordList = [['돼지고기', '퇘지고기'], ['소고기', '쇠고기'], ['부위', '부위']]
    
    lenOfWords = len(wordList)
    # print(f'lenOfWords : {lenOfWords}')
    # print(wordList)
    if lenOfWords == 1:
        return wordList
    
    resultWords = []
    preRet1 = -1
    setFirst = False
    for index in range(lenOfWords-1):
        currentGoogle = wordList[index][0]
        curruntOur = wordList[index][1]
        
        nextGoogle = wordList[index+1][0]
        nextOur = wordList[index+1][1]
        
        # print(f'currentGoogle : {currentGoogle}, curruntOur : {curruntOur}')
        # print(f'nextGoogle : {nextGoogle}, nextOur : {nextOur}')
        
        ret1, okWord1 = sumWords(currentGoogle, nextGoogle)
        ret2, okWord2 = sumWords(curruntOur, nextOur)
        
        # print(f'ret1 : {ret1}, okWord1 : {okWord1}')
        # print(f'ret2 : {ret2}, okWord1 : {okWord2}')
        
        if ret1 == True and ret2 == True:
            if preRet1 == True or setFirst == False:
                if len(resultWords) != 0:
                    resultWords.pop()
            
            resultWords.append([okWord1, okWord2])
            wordList[index+1][0] = okWord1
            wordList[index+1][1] = okWord2
            
            if setFirst == False:
                setFirst = True
        else:
            resultWords.append([currentGoogle, curruntOur])
            resultWords.append([nextGoogle, nextOur])
            
        preRet1 = ret1    
        
    resultWords2 = []
    for item in resultWords:
        doAdd = True
        for item2 in resultWords2:
            if item == item2:
                doAdd = False 
            
        # print(doAdd)
        if doAdd == True:    
            resultWords2.append(item)
            
    # print(resultWords2)
    return resultWords2

def removeSmallWord(inSentenceList):
        # 중복 단어 제거
    delWord = []
    splitWord = inSentenceList.split(' ')
    print(f'splitWord : {splitWord}')
    for word1 in splitWord:
        for word2 in splitWord:
            if word1 == word2: continue
            if word2 in word1:
                delWord.append(word2)
                
    print(f'delWord : {delWord}')
    if len(delWord) != 0:
        for word in delWord:
            try:
                splitWord.remove(word)
            except Exception as e:
                print(e)
                
    resultWord = ''.join(splitWord)
    # print(resultWord)
    return resultWord

# 세단어 이상 공백 매꿀시 아래와 같이 하면 문제가 생김...
def removeGongBak(originalWord, tWord1, tWord2):
    # 테스트 시작
    # word1 = '밀또띠아 사 줘'
    # word2 = '켁켁밀또 띠아 사 줘'
    
    # word1 = '맹동 이탈리아식 리조또 볶음밥 사 줘'
    # word2 = '맹동 이탈리아 식 리조 또 볶음밥 사 줘'
    
    splitWord = originalWord.split(' ')
    newWord1 = list(tWord1)
    newWord2 = list(tWord2)
    for split in splitWord:
        # print(f'->>>>>>>>>>>>>>>>>>>>>>split : {split}')
        # print(len(split))
        # print(len(tWord1))
        for sIndex in range(len(tWord1)):
            # print(f'pron : {tWord1[sIndex]}')
            # print(f'slice : {sIndex}, {len(split)+1}')
            
            for addIndex in range(1, 3):    
                startIndex = sIndex #0
                endIndex = sIndex+len(split)+addIndex #6
                
                tWord = tWord1[startIndex:endIndex]
                tWord2 = tWord.replace(' ', '')
                # print(f'tWord : {tWord}')
                if split == tWord2:
                    # print(f'{startIndex} to {endIndex}')
                    # print(f'sameWord2 : {tWord}')
                    
                    # gongBak = tWord.find(' ')
                    gongBak = [ x for x, y in enumerate(tWord) if y == ' ' ]
                    # print(gongBak)
                    # print(f'gongBak2 : {gongBak}')
                    
                    for gong in gongBak:
                        if gong != -1 and 0 != gong and gong != len(tWord) - 1:
                            # print('this is wanted')
                            newWord1[startIndex+gong] = ''
                            newWord2[startIndex+gong] = ''
    
    if '' in newWord1:
        newWord1.remove('')
    if '' in newWord2:
        newWord2.remove('')
    
    lastWord1 = ''.join(newWord1)
    lastWord2 = ''.join(newWord2)
    # print(f'originalWord : {originalWord}')
    # print(f'lastWord1 : {lastWord1}')
    # print(f'lastWord2 : {lastWord2}')
    
    return lastWord1, lastWord2

def makeGongBak(originalWord, tWord1, tWord2):
    # print(f'------------------------------>originalWord1 : {originalWord}')
    # print(f'------------------------------>originalWord2 : {tWord1}')
    # print(f'pret tWord1 : {tWord1}')
    # print(f'pret tWord2 : {tWord2}')
    
    splitWord = originalWord.split(' ')
    for index in range(len(splitWord)-1):
        sumWord = splitWord[index] + splitWord[index+1]
        
        if sumWord in tWord1:
            # print(f'sumWord : {sumWord}')
            searchIndex = tWord1.find(sumWord)
            addIndex = len(splitWord[index])
            # print(f'searchIndex : {searchIndex}, addIndex : {addIndex}')
            
            temp = list(tWord1)
            temp.insert(searchIndex+addIndex, ' ')
            tWord1 = ''.join(temp)
            
            temp = list(tWord2)
            temp.insert(searchIndex+addIndex, ' ')
            tWord2 = ''.join(temp)
            
    # print(f'post tWord1 : {tWord1}')
    # print(f'post tWord2 : {tWord2}')
    
    return tWord1, tWord2

# 이거 사용 안함(지우세요)
def isFillHere(oriWord, comWord, startIndex):
    preWord = []
    postWord = []
    
    for sIndex in range(startIndex-1, -1, -1):
        if comWord[sIndex] != ' ':
            preWord.append(comWord[sIndex])
        else:
            break
    for sIndex in range(startIndex+1, len(comWord)):
        if comWord[sIndex] != ' ':
            postWord.append(comWord[sIndex])
        else:
            break
    
    preWord.reverse()
    # print(f'preWord : {preWord}')
    # print(f'postWord : {postWord}')
    
    meWord = ''.join(oriWord)
    preWord.append(' ')
    taWord_gongBak = ''.join(preWord + postWord)
    preWord.remove(' ')
    taWord_append = ''.join(preWord + postWord)
    
    # print(meWord)
    # print(taWord_gongBak)
    # print(taWord_append)
    
    return True
    
    if taWord_gongBak in meWord:
        print('no Fill')
        return False
    else:
        print('yes Fill')
        return True

def spanWords(word1, word2):
    
    originalWord1 = word1.copy()
    originalWord2 = word2.copy()
    
    index1 = 0
    nextStartIndex = -1
    while True:
        
        useStartIndex = nextStartIndex + 1 
        # print(f'useStartIndex : {useStartIndex}')
        
        lastIndex = len(word2)
        for sIndex in range(index1+1, len(word1)):
            if word1[index1] != ' ' and (word1[index1] == word1[sIndex]):
            # if True and (word1[index1] == word1[sIndex]):
                # print(f'word1[index1] : {word1[index1]}, word1[sIndex] : {word1[sIndex]}')
                # lastIndex = useStartIndex + (sIndex-index1)
                lastIndex = sIndex
                
                if sIndex-1 < len(word2) and word1[index1] == word2[sIndex-1]:
                    # print(f'예외사항1 : {lastIndex}')
                    # 여기 이상합니다.
                    if word1[index1] == word2[lastIndex-1]:
                        lastIndex = lastIndex - 1
                        # print(f'예외사항2 : {lastIndex}')
                break
        
        if lastIndex > len(word2):
            lastIndex = len(word2)
            
        # print(f'lastIndex : {lastIndex}')
        
        # for index2 in range(useStartIndex, len(word2)):
        for index2 in range(useStartIndex, lastIndex):
            # print(f'lastIndex : {lastIndex}, index2 : {index2}')
            # print(f'word1[index1] : {word1[index1]}, word2[index2] : {word2[index2]}')
            if word1[index1] != ' ' and word1[index1] == word2[index2]:
            # if True and word1[index1] == word2[index2]:
            
                isSkip = False
                # print('\n')
                # print(f'검사중 {word1[index1]}')
                # print(f'Now Checking Distance is {index2-index1}\n\n')
                for checkIndex1 in range(index1+1, len(word1)):
                    for checkIndex2 in range(useStartIndex, lastIndex):
                        if word1[checkIndex1] != ' ' and word1[checkIndex1] == word2[checkIndex2]:
                            # print(f'Now Checking Word is {word1[checkIndex1]}')
                            # print(f'Future Checking Distance is {checkIndex2-checkIndex1}')
                            # if abs(index2-index1) > abs(checkIndex2-checkIndex1):
                            if abs(index2-index1) - abs(checkIndex2-checkIndex1) > 1:
                                print(f'You SKIP!!!!!!!!!!!!!!!!!!{word1[index1]}')
                                isSkip = True
                                break
                            
                    if isSkip == True:
                        # print(f'This is Break Word-1 {word1[index1]}')
                        break
                
                if isSkip == True:
                    # print(f'This is Break Word-2 {word1[index1]}')
                    break
            
                if index1 < index2:
                    # print('index1 < index2')
                    for count in range(index2-index1):
                        # 이거 해야되?말아야되?
                        # if useStartIndex == 0: useStartIndex = 1
                        word1.insert(useStartIndex, ' ')
                    
                    index1 = index1 + (index2-index1)
                    nextStartIndex = index2
                    
                elif index1 > index2:
                    # print('index1 > index2')
                    for count in range(index1-index2):
                        # 이거 해야되?말아야되?
                        # if useStartIndex == 0: useStartIndex = 1
                        word2.insert(useStartIndex, ' ')
                    
                    nextStartIndex = index1
                else:
                    # print('same')                    
                    nextStartIndex = index1
                    
                break
            else:
                # print('else')
                a = 1
                
        # print(f'word1 : {word1}, word2 : {word2}')
        
        index1 +=1
        if index1 == len(word1): break
      
    # print(f'originalWord1 : {originalWord1}')
    # print(f'originalWord2 : {originalWord2}')  
    # print(f'word1 : {word1}')
    # print(f'word2 : {word2}')
                  
    if len(word1) <= len(word2):
        for index in range(len(word1)):
            if word1[index] == ' ' and word2[index] != ' ':
                word1[index] = '켁'
                if isFillHere(originalWord1, word1, index) == False:
                    word1[index] = ' '
            elif word2[index] == ' ' and word1[index] != ' ':
                word2[index] = '꺅'
                if isFillHere(originalWord2, word2, index) == False:
                    word2[index] = ' '
    else:
        for index in range(len(word2)):
            if word1[index] == ' ' and word2[index] != ' ':
                word1[index] = '켁'
                if isFillHere(originalWord1, word1, index) == False:
                    word1[index] = ' '
            elif word2[index] == ' ' and word1[index] != ' ':
                word2[index] = '꺅'
                if isFillHere(originalWord2, word2, index) == False:
                    word2[index] = ' '
                
    return word1, word2

from hanspell import spell_checker 
def spell_check(sentence):
    sent = sentence
    spelled_sentence = spell_checker.check(sent)
    # print(f"Raw Sent : {sent}")

    hanspell_sentence = spelled_sentence.checked
    # print(f"Checked Sent : {hanspell_sentence}")

    return hanspell_sentence
    # return sentence
        
    # print(f'스펠링 체크1 :  {spell_check(newWord1)}')
    # print(f'스펠링 체크2 :  {spell_check(newWord2)}')
    
def searchInWord(searchWord, inWord):
    # test1 = '소화가잘되는우유'
    # test2 = '막소화가'
    # test3 = '잘되는'
    # test4 = '우유를'
    
    # searchWord = '소화가잘되는우유'
    # inWord = '막소화가'
    
    splitWord1 = list(searchWord)
    splitWord2 = list(inWord)
    
    sumLength = len(splitWord1) + len(splitWord2)
    # print(f'sumLength : {sumLength}')
    
    for i in range(0, len(splitWord2)):
        splitWord1.insert(0, '')
        
    for i in range(0, len(splitWord2)):
        splitWord1.append('')
    
    lastDetected = []
    for i in range(0, sumLength):
        if i != 0:
            splitWord2.insert(0, '')
        # print(splitWord1)
        # print(splitWord2)
        
        detectWord = ''
        for index in range(len(splitWord2)):
            if splitWord2[index] == splitWord1[index]:
                detectWord += splitWord2[index]
            
        # print(f'detectWord : {detectWord}')
        if detectWord != '':
            lastDetected.append(detectWord)
    
    # print(f'lastDetected : {lastDetected}')
    
    lastDetected.sort(key=len, reverse=True)
    return lastDetected
    
def sumWordAndKiwiAndSo(word1, word2, newWord1, newWord2):
    print("\n\nsumWordAndKiwiAndSo")
    
    sumWord1 = word1.replace(" ", "")
    sumWord2 = word2.replace(" ", "")

    # print(f'sumWord1 : {sumWord1}')
    # print(f'sumWord2 : {sumWord2}')
    
    kiwiSumResult1 = goSilverKiwiForSum(sumWord1)
    kiwiSumResult2 = goSilverKiwiForSum(sumWord2)
    
    print(f'kiwiSumResult1 : {kiwiSumResult1}')
    print(f'kiwiSumResult2 : {kiwiSumResult2}')
      
    splitWord1 = newWord1.split(' ')
    splitWord2 = newWord2.split(' ')
        
    print(splitWord1)
    print(splitWord2)
    
    # kiwiSumResult1 = ['소화가소화는']
    # splitWord1 = ['기소화가', '소화는', '소', '줘']
    # splitWord2 = splitWord1
            
    startIndex = []
    endIndex = []
    for sumWord in kiwiSumResult1:
        print(f'sumWord : {sumWord}')
        
        if len(sumWord) == 1:
            print('skip one word')
            continue
        
        isSkip = False
        for checkWord in splitWord1:
            if sumWord in checkWord:
                isSkip = True
        if isSkip == True:
            print('skip word')
            continue
        
        for index1 in range(len(splitWord1)-1):
            firstWord = splitWord1[index1]
            if splitWord1[index1] == '': firstWord = ' '
            
            normalCount = 1
            detectedCount = 0
            detectedWords = ''
            
            tempWord = firstWord
            detect = searchInWord(sumWord, firstWord)
            if len(detect) != 0: 
                print(f'firstWord : {firstWord}, detect1 : {detect}') 
                detectedCount += 1
                detectedWords += detect[0]
            
            for index2 in range(index1+1, len(splitWord1)):
                
                secondWord = splitWord1[index2]
                if splitWord1[index2] == '': secondWord = ' '
                
                tempWord = tempWord+secondWord
                
                normalCount += 1
                detect = searchInWord(sumWord, secondWord)
                if len(detect) != 0:
                    print(f'secondWord : {secondWord}, detect2 : {detect}') 
                    detectedCount += 1
                    detectedWords += detect[0]
                    
                # print(f'normalCount : {normalCount}, detectedCount : {detectedCount}')
                
                print(f'detectedWords : {detectedWords}, sumWord : {sumWord}')
                # if normalCount == detectedCount and sumWord in tempWord:
                if normalCount == detectedCount and detectedWords == sumWord:
                    print(f'->>>>>>>>>>>>>>>>>>>tempWord : {tempWord}, {index1, index2}')
                    startIndex.append(index1)
                    endIndex.append(index2)
    
    if len(startIndex) > 0:
        lastWord1 = ''
        for index, word in enumerate(splitWord1):            
            detect = False
            for begin, end in zip(startIndex, endIndex):
                if begin < index and index <= end:
                    lastWord1 = lastWord1 + word
                    detect = True
            if detect == False:
                if index != 0:
                    lastWord1 = lastWord1 + ' ' + word
                else:
                    lastWord1 = lastWord1 + word
                
        lastWord2 = ''
        for index, word in enumerate(splitWord2):            
            detect = False
            for begin, end in zip(startIndex, endIndex):
                if begin < index and index <= end:
                    lastWord2 = lastWord2 + word
                    detect = True
            if detect == False:
                if index != 0:
                    lastWord2 = lastWord2 + ' ' + word
                else:
                    lastWord2 = lastWord2 + word
                
        # lastWord1 = lastWord1.strip()
        # lastWord2 = lastWord2.strip()
        return lastWord1, lastWord2
    else:
        return newWord1, newWord2
    
def findGonBakString(detectWordList, refWord):
    addGoodList = []
    for word in detectWordList:
        wordList = list(word)
        
        goodList = ''
        startIndex = 0
        for index in range(1, len(wordList)+1):
            tempList = wordList.copy()
            tempList.insert(index, ' ')
            # print(f'tempList : {tempList}')
            
            lastIndex = index + 1
            if index == len(wordList): lastIndex = index
            tempList2 = tempList[startIndex:lastIndex]
            
            # print(f'tempList2 : {tempList2}')
            tempJoin = ''.join(tempList2)
            # print(f'tempJoin : {tempJoin}')
            
            if tempJoin in refWord:
                # print(f'find word : {index}')
                goodList += tempJoin
                startIndex = index
                
        addGoodList.append(goodList)
    # print(addGoodGList)
    return addGoodList

def getGoodKeyword(word1, word2):
    keyHistory = ''
    
    print(f'## 두 문장 => 1 : {word1}, 2 : {word2}\n')
    split1 = j2hcj(h2j(word1))
    split2 = j2hcj(h2j(word2))
    
    keyHistory += '## 다중 ASR 음성인식 결과 ##'+ '\n' \
                + 'ASR-1 : '+word1+'\n' \
                +split1+'\n' \
                + 'ASR-2 : '+word2+'\n' \
                +split2+'\n'
    
    # 맟춤법 검사
    # word1 = spell_check(word1)
    # word2 = spell_check(word2)
    # print('\t## 맟춤범 검사')
    # print(word1)
    # print(word2)
    
    # keyHistory += '## 맟춤법검사'+'\n'+word1+'\n'+word2+'\n'
        
    word11 = list(word1)
    word22 = list(word2)
    
    word11, word22 = spanWords(word11, word22)
        
    newWord1 = ''.join(word11)
    newWord2 = ''.join(word22)
    
    print('\t## Span Words')
    print(newWord1)
    print(newWord2)
    
    hWord1 = newWord1.replace('켁', '$').replace('꺅', '$')
    hWord2 = newWord2.replace('켁', '$').replace('꺅', '$')
    keyHistory += '## 띄어쓰기 단위로 단어정렬 ##'+'\n' \
        + 'ASR-1 : '+hWord1+'\n' \
        + 'ASR-2 : '+hWord2+'\n'
        
    # 공백 맟추기(없애기)
    newWord1, newWord2 = removeGongBak(word1, newWord1, newWord2)
    
    print('\t## 공백없앤 후 Words')
    print(f'original : {word1}')
    print(newWord1)
    print(newWord2)
        
    hWord1 = newWord1.replace('켁', '$').replace('꺅', '$')
    hWord2 = newWord2.replace('켁', '$').replace('꺅', '$')
    keyHistory += '## 공백정렬(제거) ##'+'\n' \
        + 'ASR-1 : '+hWord1+'\n' \
        + 'ASR-2 : '+hWord2+'\n'
    
    # 필요없는 단어 없애기
    newWord1 = newWord1.replace('켁', '').replace('꺅', '')
    newWord2 = newWord2.replace('켁', '').replace('꺅', '')
    print('\t## 필요없는 단어 없애기')
    print(newWord1)
    print(newWord2)
    
    keyHistory += '## 불용글자제거 ##'+'\n' \
        + 'ASR-1 : '+newWord1+'\n' \
        + 'ASR-2 : '+newWord2+'\n'
    
    # 공백 맟추기2(넣기)
    newWord1, newWord2 = makeGongBak(word1, newWord1, newWord2)
    
    print('\t## 공백넣은 후 Words')
    print(f'original : {word1}')
    print(newWord1)
    print(newWord2)
        
    keyHistory += '## 공백정렬(추가) ##'+'\n' \
        + 'ASR-1 : '+newWord1+'\n' \
        + 'ASR-2 : '+newWord2+'\n'
    
    # 다 더해서 형태소 나온결과를 보고 다시 정렬해주기
    # 여기서 하는 일은 다 붙여서 나오는 결과를 이용해서 떨어진거 붙여주기. 형태소를 돌린것이 아님.
    print('\t## 다 더해서 형태소 돌려보기')
    newWord1, newWord2 = sumWordAndKiwiAndSo(word1, word2, newWord1, newWord2)
    print(f'original : {word1}')
    print(newWord1)
    print(newWord2)
        
    # keyHistory += '## 공백제거 NER상품명 검색결과 ##'+'\n'+newWord1+'\n'+newWord2+'\n'
    
    # 형태소 돌리기
    splitWord1 = newWord1.split(' ')
    splitWord2 = newWord2.split(' ')
    
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    print(f'splitWord1 : {splitWord1}')
    print(f'splitWord2 : {splitWord2}')
    
    lastWords = []
    lastWordsForDebug = []
    
    # for wIndex in range(len(splitWord1)):
        
    #     kiwiResult, _ = goSilverKiwi(splitWord1[wIndex])
    #     print(f'kiwiResult : {kiwiResult}')
    #     print('\n\n')
        
    #     if len(kiwiResult) > 0 and kiwiResult[0] != '':
            
    #         lastResult = ''
    #         for res in kiwiResult:
    #             lastResult += res 
    #         # lastWords.append([result[0], splitWord2[wIndex]])
            
    #         kiwiResult2, _ = goSilverKiwi(splitWord2[wIndex])
            
    #         lastResult2 = ''
    #         if len(kiwiResult2) > 0:
    #             print(f'kiwiResult2 : {kiwiResult2[0]}')
    #             if len(kiwiResult2) < 1:
    #                 print('length is long----------------------------------------------------------------->')
    #             for res2 in kiwiResult2:
    #                 lastResult2 += '' + res2
    #             lastResult2 = lastResult2.strip()
    #         else:
    #             print('No Word')
    #             lastResult2 = ''
            
    #         print(f'lastResult : {lastResult}, lastResult2 : {lastResult2}')
    #         lastWords.append([lastResult, lastResult2])
    
    kiwiResultForDebug1 = []
    kiwiResultForDebug2 = []
    for wIndex in range(len(splitWord1)):
        
        kiwiResult, _, kiwiTotalResult = goSilverKiwi(splitWord1[wIndex])
        print(f'kiwiResult : {kiwiResult}')
        
        lastResult = ''
        if len(kiwiResult) > 0 and kiwiResult[0] != '':
            for res in kiwiResult:
                lastResult += res 
            lastResult = lastResult.strip()
          
        try:  
            print(f'splitWord2[wIndex] : {splitWord2[wIndex]}')
            kiwiResult2, _, kiwiTotalResult2 = goSilverKiwi(splitWord2[wIndex])
            print(f'kiwiResult2 : {kiwiResult2}')
            
            lastResult2 = ''
            if len(kiwiResult2) > 0 and kiwiResult2[0] != '':
                for res2 in kiwiResult2:
                    lastResult2 += '' + res2
                lastResult2 = lastResult2.strip()
        except Exception as e:
            print(f'Exception : {e}')
            lastResult2 = ''
            kiwiTotalResult2 = []
            
        print(f'lastResult : {lastResult}, lastResult2 : {lastResult2}')
        print(f'kiwiTotalResult : {kiwiTotalResult}, kiwiTotalResult2 : {kiwiTotalResult2}')
        
        for res in kiwiTotalResult:
            kiwiResultForDebug1.append([res.form, res.tag])
        for res in kiwiTotalResult2:
            kiwiResultForDebug2.append([res.form, res.tag])     
        
        if lastResult != '' or lastResult2 != '':
            lastWords.append([lastResult, lastResult2])

        # 값 자체가 없을경우, 위에서 이미 에러 남
        try:
            if lastResult == '': lastResult = '<'+ splitWord1[wIndex] + '>'
        except Exception as e:
            print(f'Exception1 : {e}')
        try:
            if lastResult2 == '': lastResult2 = '<' + splitWord2[wIndex] + '>'
        except Exception as e:
            print(f'Exception2 : {e}')
        lastWordsForDebug.append([lastResult, lastResult2])
        
    print(f'kiwiResultForDebug1 : {kiwiResultForDebug1}')
    print(f'kiwiResultForDebug2 : {kiwiResultForDebug2}')
    print(f'lastWordsForDebug : {lastWordsForDebug}')
    
    # 형태소 분석 결과 추가
    # kiwiResultForDebug1
    keyHistory += '## 형태소 분석 결과 ##' + '\n'
    keyHistory += 'ASR-1 : ' + newWord1 + " : "
    for kResut in kiwiResultForDebug1:
        tag = kResut[1]
        ment = '비상품명'
        if tag == 'NNP': ment = '상품명'
        keyHistory += f'({kResut[0]}, {ment})'
    keyHistory += '\n'
    keyHistory += 'ASR-2 : ' + newWord2 + " : "
    for kResut in kiwiResultForDebug2:
        tag = kResut[1]
        ment = '비상품명'
        if tag == 'NNP': ment = '상품명'
        keyHistory += f'({kResut[0]}, {ment})'
    keyHistory += '\n'
            
    # keyHistory += '## 형태소결과 ##' + '\n'
    keyHistory += '## 공백제거 NER상품명 검색결과 ##'+'\n'
    # keyHistory += '## 공백생성 NER상품명 검색결과 ##' + '\n'
    keyHistory += 'ASR-1 : '
    for word in lastWords:
        keyHistory += word[0] + ' '
    keyHistory += '\n'
    keyHistory += 'ASR-2 : '
    for word in lastWords:
        keyHistory += word[1] + ' '
    keyHistory += '\n'
    
    matchingWords = [newWord1, newWord2]
    print(lastWords)
        
    # 원래 떨어져 있는 단어 가져오기...
    gWords = []
    oWords = []
    for word in lastWords:
        gWords.append(word[0])
        oWords.append(word[1])
        
    addGoodGList = findGonBakString(gWords, word1)
    addGoodOList = findGonBakString(oWords, word2)
    
    print(f'addGoodGList : {addGoodGList}')
    print(f'addGoodOList : {addGoodOList}')
    
    for index in range(len(addGoodGList)):
        if lastWords[index][0] != '':
            if lastWords[index][0] == addGoodGList[index]:
                lastWords[index][0] += '#' + addGoodGList[index] #이거 추가?말어?
            else:    
                lastWords[index][0] += '#' + addGoodGList[index]
    for index in range(len(addGoodOList)):
        if lastWords[index][1] != '': 
            if lastWords[index][1] == addGoodOList[index]:
                lastWords[index][1] += '#' + addGoodOList[index] #이거 추가?말어?
            else:
                lastWords[index][1] += '#' + addGoodOList[index]
    # keyHistory += '## 떨어진 단어 추가' + '\n'
    
    print(f'마지막 리턴 결과(정리 전) : {lastWords}')
    
    gLastSentence = ''
    oLastSentence = ''
    for index, word in enumerate(lastWords):
        addGongBak = ' '
        if index == 0: addGongBak = ''
        
        print(f'{index} addGongBak : [{addGongBak}]')
        
        if word[0] != '':
            gLastSentence += addGongBak + word[0].split('#')[0].strip()
        if word[1] != '':
            oLastSentence += addGongBak + word[1].split('#')[0].strip()
        
    print(f'oLastSentence1 : [{oLastSentence}]')
        
    gLastSentence += '#'
    oLastSentence += '#'
    
    for index, word in enumerate(lastWords):
        addGongBak = ' '
        if index == 0: addGongBak = ''
        
        if word[0] != '':
            gLastSentence += addGongBak + word[0].split('#')[1].strip()
        if word[1] != '':
            oLastSentence += addGongBak + word[1].split('#')[1].strip()
        
    gLastSentence = gLastSentence.replace('# ', '#')
    oLastSentence = oLastSentence.replace('# ', '#')
    if gLastSentence == '#': gLastSentence = ''
    if oLastSentence == '#': oLastSentence = ''
        
    lastWords = [[gLastSentence, oLastSentence]]
    
    randomSwap = False
    randomInt = random.randrange(1,3)
    if randomInt == 2:
        randomSwap = True
        
    print(f'randomInt : {randomInt}')
    # randomSwap = True
    if randomSwap == True:
        # 위의 스트링 모두 뒤집기
        # lastWord 뒤집기
        # lastWordsForDebug 뒤집기
        print('*****************************\n\n\n')
        print(keyHistory)
        print(lastWords)
        print(lastWordsForDebug)
        print('*****************************\n\n\n')
        
        import io
        buf = io.StringIO(keyHistory)
        
        newHistory = ''
        while True:
            read = buf.readline()
            if not read:
                break
            # print(read.replace('\n', ''))
            
            if "ASR-1" in read:
                temp = read.replace('ASR-1', 'ASR-2')
                count = 0
                while True:
                    read2 = buf.readline()
                    if "ASR-2" in read2:
                        if count == 1:
                            newHistory += read2.replace('ASR-2', 'ASR-1') + buf.readline() + temp
                        else:
                            newHistory += read2.replace('ASR-2', 'ASR-1') + temp
                        break
                    else:
                        temp += read2
                        
                    count += 1
            else:
                newHistory += read
        keyHistory = newHistory
        
        temp1 = lastWords[0][0]
        temp2 = lastWords[0][1]
        lastWords = [[temp2, temp1]]
        
        lastWordsForDebugTemp = []
        for partList in lastWordsForDebug:
            temp1 = partList[0]
            temp2 = partList[1]
            
            tempList = [temp2, temp1]
            lastWordsForDebugTemp.append(tempList)
        lastWordsForDebug = lastWordsForDebugTemp
        
        print('\n\n\n*****************************')
        # 위의 스트링 모두 뒤집기

    print(f'마지막 리턴 결과 : {lastWords}')
    keyHistory += '## 공백생성 NER상품명 검색결과 ##' + '\n'
    try:
        gongWord1 = lastWords[0][0].split('#')[1]
    except Exception as e:
        print(e)
        gongWord1 = ''
        
    try:
        gongWord2 = lastWords[0][1].split('#')[1]
    except Exception as e:
        print(e)
        gongWord2 = ''
        
    diffWord1 = lastWords[0][0].split('#')[0]
    diffWord2 = lastWords[0][1].split('#')[0]
    
    keyHistory += 'ASR-1 : '
    if gongWord1 == '': keyHistory += diffWord1 + '\n'
    else : keyHistory += gongWord1 + '\n'

    keyHistory += 'ASR-2 : '
    if gongWord2 == '': keyHistory += diffWord2 + '\n'
    else : keyHistory += gongWord2 + '\n'
    
    similarity = -1
                
    if diffWord1 == '' and diffWord2 != '':
        keyHistory += '## 처리결과 ##' + '\n'
        keyHistory += f"ASR-1이 NER 상품명에 등재돼어 있지 않아 검색어 제외 및 \"{diffWord2}\"을(를) 화자에게 확인" + '\n'
    elif diffWord1 != '' and diffWord2 == '':
        keyHistory += '## 처리결과 ##' + '\n'
        keyHistory += f"ASR-2가 NER 상품명에 등재돼어 있지 않아 검색어 제외 및 \"{diffWord1}\"을(를) 화자에게 확인" + '\n'
    elif diffWord1 == '' and diffWord2 == '':
        keyHistory += '## 처리결과 ##' + '\n'
        keyHistory += f"ASR-1과 ASR-2 둘 다 NER 상품명에 등재돼어 있지 않아 자식에게 물어봄" + '\n'
    else:
        similarity = diff(diffWord1, diffWord2)
        similarity = similarity * 100
        similarity = int(similarity)
        print(similarity)
        
        keyHistory += f"## NER 상품명들의 자모유사도 분석 결과 ##" + '\n'
        keyHistory += f'유사도 {similarity}%' + '\n'
        
        keyHistory += '## 처리결과 ##' + '\n'
        if similarity == 100:
            keyHistory += f"100% 일치하므로 화자에게 \"{diffWord1}\"가(이) 맞는지 확인" + '\n'
        else:
            if similarity >= 70:
                keyHistory += f"70% 이상의 결과로 화자에게 \"{diffWord1}\" 인지 \"{diffWord2}\" 인지 chatbot 문의" + '\n'
            else:
                # 뒤집어 지면 아래 diffWord1을 diffWord2로 바꿔줌
                if randomSwap == True:
                    value = diffWord2
                else:
                    value = diffWord1
                keyHistory += f"70% 이하의 결과로 화자에게 \"{value}\"가(이) 맞는지 확인" + '\n'
    
    print(keyHistory)

    debugWord1 = ""
    debugWord2 = ""
    if lastWords[0][0] != '' and lastWords[0][1] == '':
        splitWord = lastWords[0][0].split('#')[0].split(' ')
        for spWord in splitWord:
            for cpWord in lastWordsForDebug:
                if cpWord[0] == spWord:
                    debugWord1 += ' ' + spWord
                    debugWord2 += ' ' + cpWord[1]
                    
        debugWord2 = debugWord2.replace('<', '').replace('>', '').strip()
        debugWord2 = '<' + debugWord2 + '>'
        lastWords[0][1] = debugWord2
    elif lastWords[0][0] == '' and lastWords[0][1] != '':
        splitWord = lastWords[0][1].split('#')[0].split(' ')
        for spWord in splitWord:
            for cpWord in lastWordsForDebug:
                if cpWord[1] == spWord:
                    debugWord1 += ' ' + cpWord[0]
                    debugWord2 += ' ' + spWord
        debugWord1 = debugWord1.replace('<', '').replace('>', '').strip()
        debugWord1 = '<' + debugWord1 + '>'           
        lastWords[0][0] = debugWord1
                    
    if similarity != -1 and similarity < 70:
        if randomSwap == True:
            tempWord = '!' + lastWords[0][0] + '!'
            lastWords[0][0] = tempWord
        else:
            tempWord = '!' + lastWords[0][1] + '!'
            lastWords[0][1] = tempWord
        
    print(f'lastWords : {lastWords}')
    return lastWords, keyHistory

if __name__ == '__main__':    
    
    # word1 = '나는 너를 커피 믹스 사고 싶어' #굵은소금 #길이가 더 짧으면으로 처리?
    # word2 = '나는 너의 카피맥스 사고 싶어' #구은소금
    # word1 = '나는 참치회 먹고 싶어' #굵은소금
    # word2 = '너 의 첨치 회 사고싶어요ㅎㅎㅎ' #구은소금 ->>>>>>>>>>>>>>>>>이거 이상함 '너'가 지워짐??????
    # word1 = '카레용 돼지고기 부위 알려 줘'
    # word2 = '카레용 돼지고기 부위 알려 줘'
    
    # 이거 다시 잘 생각해보자고요....
    # word1 = '짜장면용 사주시오'
    # word2 = '쩌장면 용 면 사주시오' # ->>>>>>>>>>>>>>>>>>>>>>>이거 희한하게 되네? 이거 안 됨 
    # word1 = '짜장면 용 면 사줘'
    # word2 = '쩌장면 용 면 사주삼'
    # word1 = '김 용 재료삼 사주세삼' #not perfect
    # word2 = '곰 용 재료 사주 삼' #not perfect ->>>>>>>>>>>>>>>>>>>>>>>>>이거 안되네? 중간에 이빨 빠져서...
    # word1 = '스펨 감자찌게 사주세요' #둘다 틀렸을 경우임 째게 => 찌개
    # word2 = '스팸 김치찌게 사주'
    # word1 = '명란 계란말이 말아조' #이거 어려움
    # word2 = '밍탄 계란마리 마라조' # ->>>>>>>>>>>>>>>>>>>>>>>>>>>이거도 안되네? 뒤 끝까지 안 보게 했으나, 이상하게 될 문제가 생길수 있음
    
    # word1 = '나는 참치회 먹고 싶어'
    # word2 = '나 아 첨치 회 사고 싶어욯ㅎㅎㅎ'
    # word1 = '나 아 첨치 회 사고 싶어욯ㅎㅎㅎ'
    # word2 = '나는 참치회 먹고 싶어' #뒷문장 짤리
    # word1 = '쩌장면용 사줘'
    # word2 = '짜장면 용 사주삼'
    # word1 = '짜장면용 사주시오'
    # word2 = '짜장면 용 사주삼'
    
    # 이것도 문제가 되네요 20230105
    # word1 = '나는 참치회 먹고 싶어'
    # word2 = '너 아이고 첨치 회 사고싶어욯ㅎㅎㅎ'
    
    # word1 = '나 아이 첨치 회 사고싶어욯ㅎㅎㅎ'
    # word2 = '나는 참치회 먹고 싶어'
    
    # word1 = '나는 광어회 먹고 싶어'
    # word2 = '나는 첨치회 사고싶어요ㅎㅎㅎ'
    
    # word1 = '말을 아라리오 참치 해' #잘못 인식 됨, 이럴경우 못 알아 듣는 거라 다시 물어 봐야 함
    # word2 = '말을 하면 참취해' 
    
    # 이것도 문제가 되네요
    # word1 = '맛있는 짜장면 사 줘'
    # word2 = '짜장면 사 줘'
    
    # 이거 좀더 자세히 분석해보자->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # word1 = '맛있는 보리 찾아 줘'
    # word2 = '맛있는 보리차 사줘'

    # 이거 좀더 자세히 분석해보자->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # word1 = '맹동 이탈리아식 리조또 볶음밥 사 줘'
    # word2 = '냉동 이탈리아 식기조 또 볶음밥 사줘'

    # 이거 좀더 자세히 분석해보자->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # word1 = '밀또띠아 사 줘'
    # word2 = '미를 또 뛰야 사줘'
    
    # word1 = '사리곰탕면'
    # word2 = '살이 검탕면'
    
    # word1 = '버로 먹는 불고기샐러드 화성시 사 줘'
    # word2 = '바 아 먹는 불고기 샐러드와 소스 사줘'
    
    # 이거 좀더 자세히 분석해보자->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # word1 = '아 만나서 죽'
    # word2 = '아 만나 사죽'
    
    # word1 = '병천 카카오 주스 음료수 사 줘'
    # word2 = '병천 카카오 주스 음료 수 사 줘'
    
    # word1 = '학교 불릴필요없는 발효 현미'
    # word2 = '학교 불릴 필요 없는 발효 현미'
    
    # 문자 매칭 실패->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # 20230105
    # word1 = '마요네즈가 버터밀크 섞인 샐러드용으로 사 줘'
    # word2 = '마요네즈와 버터밀크가 서김 샐러드용 렌치 소스 사줘'
    
    # word1 = '새우까스'
    # word2 = '새우가스'
    
    # word1 = '소화가잘되는우유'
    # word2 = '막소화가 잘되는 우유를'
    
    # word1 = '아리야 막막막소화가 잘되는 우유를 사줘요'
    # word2 = '마실아 막소화가 잘되는 우유를 사줘요'
    
    # word1 = '나는 삼겹살 보쌈용 소화가 잘되는 우유 사고싶어'
    # word2 = '너의 삼겹살 쌈용 소화가 잘되는 우유 싶어'
    
    # word1 = '사퇴 사줘'
    # word2 = '사태 사줘'
    
    # word1 = '돼지고기 다진 것'
    # word2 = '돼지고기 다진 것'
    
    # word1 = '보쌈'
    # word2 = '부쌈'
    
    # word1 = '등심돈가스'
    # word2 = '증신분가습'
    
    # word1 = '매운 닭강정'
    # word2 = 'NO 정'

    # word1 = '코끼리 김치'
    # word2 = '고끼리 고치'
        
    # word1 = '감자 참치찌게'
    # word2 = '김치 삼치찌개'
    
    word1 = '돼지고기 앞다리살 한 근'
    word2 = '돼지고기 앞다릿살 한금'
        
    # sumWordAndKiwiAndSo('','','','')
    # exit(0)
                
    result, history = getGoodKeyword(word1, word2)
    print(f'result : {result}')
    # print(history)
    
    exit(0)
    
    # # 형태소 돌려서 명사만 추출
    # word1 = goSilverKiwi(word1)
    # word2 = goSilverKiwi(word2)
    
    # word1 = ' '.join(word1)
    # word2 = ' '.join(word2)
    
    # print(word1)
    # print(word2)
    
    # # 중복 단어 제거
    # word1 = removeSmallWord(word1)
    # word2 = removeSmallWord(word2)
    
    # print(f'중복제거1 : {word1}')
    # print(f'중복제거2 : {word2}')
    # print('\n')
    # exit(0)
            
    # 1. 여러 조합으로 만들기(현재는 2단어만 붙이기) (순서가 결과에 영향)
    result1 = makeCompareWord(word1)
    result2 = makeCompareWord(word2)
    
    print('makeCompareWord => 두단어 조합으로 만들기')
    print(result1)
    print(result2)
    print('\n')
    
    # 명사인지 확인 후 비교 시작...
    # 70프로 비슷한 단어 매칭하기...
    result = wordMatching(result1, result2)
    print('wordMatching => 70프로 기준 단어 매칭하기')
    print(result)
    print('\n')
    
    # # 두단어 붙였을 때 같은 항목 제거 (구글꺼 기준으로만 함) (순서가 결과에 영향)
    # result = cleanList(result)
    # print('cleanList => 두단어 붙였을 때 중복 제거')
    # print(result)
    # print('\n')
    
    # 짧은 단어가 같은게 있으면 제거 (구글꺼 기준으로만 함)
    result = cleanList2(result)
    print('cleanList2 => 중복으로 있는 짧은 단어 제거')
    print(result)
    print('\n')
                        
    # 형태소 돌린 후 중복 제거 
    result = removeSame(result)
    print('removeSame => 단순 중복 제거')
    print(result)
    print('\n')
       
    # 앞뒤로 겹치는 단어 합치기 (구글꺼 기준으로만 함) (순서가 결과에 영향)
    result = sumWordsAll(result)
    print('sumWordsAll => 앞뒤로 겹치는 단어 합치기')
    print(result)
    print('\n')
    
    # # 형태소 돌려서 명사만 추출
    # result = doKiwi(result)
    # print('doKiwi = > 형태소 돌려서 명사만 추출')    
    # print(result)    
    # print('\n')
    
    # 맟춤법 및 띄어쓰기 보정
    result = checkSpell(result)
    print('checkSpell => 맟춤범 검사(띄어쓰기 보정)')
    print(result)
    print('\n')
    
    
    # exit(0)
    
    # allDict = ''
    # with open('myDict.dict', 'r') as fr:
    #     while True:
    #         read = fr.readline()
    #         if not read: break
    #         allDict += ' ' + read.split('\t')[0]

    # wordSplit1 = word1.split(' ')
    # wordAppend = ''
    # for word in wordSplit1:
    #     if word in allDict:
    #         wordAppend += ' ' + word

    # print(wordAppend) 
    
    # wordSplit2 = word2.split(' ')
    # wordAppend2 = ''
    # for word in wordSplit2:
    #     if word in allDict:
    #         wordAppend2 += ' ' + word

    # print(wordAppend2)    
    
    # word1 = wordAppend
    # word2 = wordAppend2
    
    # exit(0)