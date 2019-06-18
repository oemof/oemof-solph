#!/bin/sh

errorlog_file="/tmp/doc_errors.log"

sphinx-build -q doc/ doc/_build/ 2> ${errorlog_file} >/dev/null

numerrors=`grep -icE 'error|warning' ${errorlog_file}`

echo ""
cat ${errorlog_file}

if [ ${numerrors} -ne 0 ]; then
  echo Doc creation produced ${numerrors} errors and warnings.
  exit 1
fi

