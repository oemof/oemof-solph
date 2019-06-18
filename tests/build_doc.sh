#!/bin/sh

numerrors=`sphinx-build -q doc/ doc/_build/ 2>&1 >/dev/null | grep -ic 'error'`

if [ ${numerrors} -ne 0 ]; then
  exit 1
fi

