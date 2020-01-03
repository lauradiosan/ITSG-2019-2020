//
//  ViewController.swift
//  CaltechConverter
//
//  Created by Tudor-Dan Balas on 31/10/2019.
//  Copyright © 2019 ProjectBit. All rights reserved.
//

import Cocoa

class ViewController: NSViewController {

    
    private var outputDict: [String: [Annotation]] = [:]
    
    override func viewDidLoad() {
        super.viewDidLoad()
        startAlgo()
        printOutput()
    }

    override var representedObject: Any? {
        didSet {
        }
    }

    private func getDocumentsDirectory() -> URL {
        let paths = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)
        return paths[0]
    }
    
    private func printOutput() {
        var str = "[\n"
        let filename = getDocumentsDirectory().appendingPathComponent("output.txt")
        
        let sortedKeys = Array(outputDict.keys).compactMap { Int($0) }.sorted(by: <).compactMap { String($0) }
        for key in sortedKeys {
            let annotationArr = outputDict[key]!
            
            let adjustedKey = Int(key)! - 1
            str +=
            """
                {
                    "image": "\(imageNameBuilder(string: adjustedKey))",
                    "annotations": [
            
            """
            
            for currentIndex in 0 ..< annotationArr.count {
                if currentIndex == annotationArr.count - 1 {
                    str +=
                    """
                            {
                                "label": "\(annotationArr[currentIndex].label)",
                                "coordinates": {
                                    "x": \(annotationArr[currentIndex].coordinates[0])
                                    "y": \(annotationArr[currentIndex].coordinates[1])
                                    "width": \(annotationArr[currentIndex].coordinates[2])
                                    "height": \(annotationArr[currentIndex].coordinates[3])
                                }
                            }
                    
                    """
                } else {
                    str +=
                    """
                            {
                                "label": "\(annotationArr[currentIndex].label)",
                                "coordinates": {
                                    "x": \(annotationArr[currentIndex].coordinates[0])
                                    "y": \(annotationArr[currentIndex].coordinates[1])
                                    "width": \(annotationArr[currentIndex].coordinates[2])
                                    "height": \(annotationArr[currentIndex].coordinates[3])
                                }
                            },
                    
                    """
                }
            }
            str +=
            """
                    ]
                },
            
            """
            
            
            
        }
        str = String(str.dropLast(2))
        str +=
        """
        
        ]
        """
        do {
            try str.write(to: filename, atomically: true, encoding: String.Encoding.utf8)
        } catch {
            // failed to write file – bad permissions, bad filename, missing permissions, or more likely it can't be converted to the encoding
        }
        
    }

    private func startAlgo() {
        var arr = [String]()
        if let wordsURL = Bundle.main.url(forResource: "V000", withExtension: "txt") {
            if let words = try? String(contentsOf: wordsURL) {
                arr = words.components(separatedBy: CharacterSet(charactersIn: " \n"))
            }
        }
        processArr(arr)
    }
    
    private func processArr(_ arr: [String]) {
        var splits = [Int]()
        for index in 0 ..< arr.count {
            if arr[index].contains("--------------------------------") { splits.append(index) }
        }
        splits.append(arr.count - 1)
        for index in 0 ..< splits.count - 1 {
            
            var lblUnwrapped: String
            var strUnwrapped: Int
            var endUnwrapped: Int
            var posUnwrapped: [Double]
            (lblUnwrapped, strUnwrapped, endUnwrapped, posUnwrapped) = handleChunk(arr: arr, startIndex: splits[index], endIndex: splits[index + 1])
            
            var contor = 0
            for position in strUnwrapped ... endUnwrapped {
                let currentPos = Array(posUnwrapped[contor...contor+3])
                let annotation = Annotation(label: lblUnwrapped, coordinates: currentPos)
                
                contor += 4
                
                let stringPosition = String(position)
                if outputDict[stringPosition] == nil {
                    outputDict[stringPosition] = [annotation]
                } else {
                    var arr = outputDict[stringPosition]
                    arr?.append(annotation)
                    outputDict[stringPosition] = arr
                }
            }
            
        }
    }
    
    private func handleChunk(arr: [String], startIndex: Int, endIndex: Int) -> (String, Int, Int, [Double]) {
        var lbl: String?
        var str: Int?
        var end: Int?
        var pos: [Double]?
        var mutableStartIndex = startIndex
        while mutableStartIndex <= endIndex {
            if arr[mutableStartIndex].contains("lbl") {
                lbl = handleLabel(arr[mutableStartIndex])
                mutableStartIndex += 1
            } else if arr[mutableStartIndex].contains("str") {
                str = Int(handleStr(arr[mutableStartIndex]))
                mutableStartIndex += 1
            } else if arr[mutableStartIndex].contains("end") {
                end = Int(handleEnd(arr[mutableStartIndex]))
                mutableStartIndex += 1
            } else if arr[mutableStartIndex].contains("pos") {
                mutableStartIndex += 1
                pos = handleCoords(arr, startIndex: mutableStartIndex, endIndex: endIndex)
                mutableStartIndex = endIndex + 1
            } else {
                mutableStartIndex += 1
            }
        }
        guard let lblUnwrapped = lbl, let strUnwrapped = str, let endUnwrapped = end, let posUnwrapped = pos else { fatalError("Something is not initialized")}
        return (lblUnwrapped, strUnwrapped, endUnwrapped, posUnwrapped)
    }
    
    private func imageNameBuilder(string: Int) -> String {
        return imageNameBuilder(string: String(string))
    }
    
    private func imageNameBuilder(string: String) -> String {
        let numberOfZeros = 5 - string.count
        let zeros = String(repeating: "0", count: numberOfZeros)
        return "I\(zeros)\(string).jpg"
    }
}

extension ViewController {
    fileprivate func handleLabel(_ str: String) -> String {
        return String(str.dropLast(1).dropFirst(5))
    }
    
    fileprivate func handleStr(_ str: String) -> String {
        return String(str.dropFirst(4))
    }
    
    fileprivate func handleEnd(_ str: String) -> String {
        return String(str.dropFirst(4))
    }
    
    fileprivate func handleCoords(_ arr: [String], startIndex: Int, endIndex: Int) -> [Double] {
        var mutableStartIndex = startIndex
        var res = [Double]()
        
        while mutableStartIndex < endIndex {
            var firstStr = arr[mutableStartIndex]
            if arr[mutableStartIndex] == "]" { break }
            if arr[mutableStartIndex].starts(with: "=[") {
                firstStr = String(arr[mutableStartIndex].dropFirst(2))
            }
            
            res.append((firstStr as NSString).doubleValue)
            
            for index in mutableStartIndex+1 ... mutableStartIndex+2 {
                res.append((arr[index] as NSString).doubleValue)
            }
            
            var lastStr = arr[mutableStartIndex+3]
            if lastStr.last == ";" {
                lastStr = String(arr[mutableStartIndex+3].dropLast(1))
            }
            res.append((lastStr as NSString).doubleValue)
            mutableStartIndex += 4
        }
        
        
        return res
    }
}

class Annotation {
    
    var label: String
    var coordinates: [Double]
    
    init(label: String, coordinates: [Double]) {
        self.label = label
        self.coordinates = coordinates
    }
}
