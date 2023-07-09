#!/bin/bash
agbenchmark start --maintain --mock
agbenchmark start --improve --mock
agbenchmark start --mock
agbenchmark start --mock --category=retrieval
agbenchmark start --mock --category=regression
agbenchmark start --mock --category=interface
agbenchmark start --mock --category=code
agbenchmark start --mock --category=memory
agbenchmark start --mock --category=memory --category=code
