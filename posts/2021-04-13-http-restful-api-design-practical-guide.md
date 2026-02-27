---
title:  "RESTful API Design — A practical guide"
date:   2021-04-13 20:00:00 +0800
author: HoMuChen
pin: true
description: 此系列文章是Restful API design的教學目錄，將從什麼是API、怎樣是好的API、HTTP協議、RESTful是什麼、以及其他許多當你在設計API時會遇到情況，例如\:Documentation、Pagination、Rate Limiting、Monitoring．
last_modified_at: 2022-06-07 00:07:00 +0800
category: Web Development
tags: [api, http, restful api]
---

此篇文章將作為接下來一系列關於Restful API design的目錄．

**Part 1:** 將介紹什麼是API，何時需要他，以及怎樣才會是一個好的API．

**Part 2:** 在許多種API中，此系列只專注於HTTP RESTful API，為了更好地學習他，必須先了解HTTP Protocol，知道其中各個組成HTTP Message的每一個部分．

**Part 3:** 介紹何為RESTful API，為什麼他會長這樣，以及其他許多當你在設計API時會遇到情況，例如: Documentation、Pagination、Rate Limiting、Monitoring．

**Part 4:** 陸續想到一些相關的議題，再放上來！

## Outline
1. Introduction
   * 1.1 What is an API?
   * 1.2 What is a good API?
2. HTTP Basics
   * [2.1 A HTTP Overview](/posts/http-introduction-telnet-nc-curl/)
   * [2.2 HTTP Methods](/posts/http-methods-which-to-use-and-how-to-use-them-correctly/)
   * [2.3 HTTP Response status codes](/posts/http-response-status-codes-how-to-use/)
   * [2.4 HTTP URI](/posts/what-is-url-and-what-is-it-composed-of/)
   * [2.5 HTTP Headers](/posts/http-headers/)
   * [2.6 [Practices] A HTTP client — curl](/posts/linux-http-client-tool-curl-usage/)
3. RESTful API and some Practical Guidelines
   * [3.1 What is a RESTful API?](/posts/restful-api-introduction/)
   * [3.2 Identifying Resources](/posts/restful-api-how-to-design-paths-and-identify-resources/)
   * [3.3 API first principle and an introduction to OpenAPI](/posts/api-first-principle-openapi/)
   * [3.4 [Practices] How do I manage a large OpenAPI spec file?](/posts/how-to-manage-a-large-openapi-document-file/)
   * [3.5 Pagination](/posts/restful-api-pagination/)
   * 3.6 Rate Limiting
   * 3.7 Monitoring
4. Advanced Topics
   * 4.1 Connection management
   * 4.2 Resource Modeling: Fine-grained or Coarse-grained?
   * 4.3 Versioning and Compatibility
   * 4.4 How to Response to a Health Check?
