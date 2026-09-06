+++
draft = true
date = 2023-04-22T04:57:42+01:00
title = "Floating Points"
description = ""
slug = ""
tags = []
categories = []
externalLink = ""
series = []
+++

in nowadays increasingly technology-oriented society, humans make sure
claims based on relatively un-precise computations. We are constantly
quantifying our world, estimating some parameters that are important
to us: the speed of cars when we want to know if it's safe to cross
the road, the price of things we buy, the level of investment we
should make, etc. All these computations are made with and generate
what mathematicians call **real numbers**: the infinitely continuous
set of numbers that allow for more precise quantification of our
world, more than what was made possible with **natural numbers** (1,
2, 5, 7, etc.). In one of my recent coding works, I had to convert a
numerical quantity from one storage format to another, and compare the
two to make sure the conversion didn't make me lose any
precision. Well, I was surprised to see that it actually did: about 5%
precision lost. One immediate remarks I made was that both formats
were not using the same precision for the representation of the
quantity. That made me think about what computers use for representing
real numbers, and how, as precise as it is, remains quite *fragile*
nonetheless. This article is for exploring that idea a little bit.

## Representing real numbers

In a previous article{{< ref "reflections.md" >}} (in french), I
talked about the birth of natural numbers and how they are represented
in our language, and later on on our computers: by use of the binary
number system. For natural numbers, this is pretty straight forward.

This happens
because floating point arithmetic is the standard that sustains
computation over real numbers, governing all the quantifications that
our society relies upon. We are constantly rounding, in every single
one of our computation, accumulating errors that grow as small
programs keep building on top of each other.

## Why it works


## Practical example: Python
