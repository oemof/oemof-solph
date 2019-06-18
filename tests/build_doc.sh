#!/bin/sh

errorlog_file="/tmp/doc_errors.log"

sphinx-build -q doc/ doc/_build/ 2> ${errorlog_file} >/dev/null

numerrors=`grep -icE 'error|warning' ${errorlog_file}`


if [ ${numerrors} -ne 0 ]; then
  echo "Doc creation error log:"
  sed 's/^/>\t/' ${errorlog_file}
  echo ""
  echo ""
  echo "Doc creation produced ${numerrors} errors and warnings."
  exit 1
fi

