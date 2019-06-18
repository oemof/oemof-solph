#!/bin/sh

errorlog_file="doc_errors.log"

sphinx-build -q doc/ doc/_build/ 2> doc_errors.log >/dev/null

numerrors=`grep -icE 'error|warning' ${errorlog_file}`

if [ ${numerrors} -ne 0 ]; then
  echo Doc creation produced ${numerrors} errors and warnings:
  echo ""
  cat ${errorlog_file}
  exit 1
fi

