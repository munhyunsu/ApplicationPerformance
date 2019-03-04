data = read.csv('/home/harny/Github/ApplicationPerformance/AppTimingIndex/output/com.amazon.mShop.android.shopping.pcap.csv', header=TRUE)

png('waterfall.png', width = 1280, height = length(as.matrix(data[1]))*25+20)
temp_par = par()
par(mar = c(6, 5, 5, 4)+0.1)
par(xpd = TRUE)

header = c('domainLookupStart', 'domainLookupEnd', 'connectStart', 
           'connectEnd', 'secureConnectionStart', 'requestStart', 
           'responseStart', 'responseEnd')

barplot(t(as.matrix(data[5])),
        horiz=TRUE,
        names.arg=as.matrix(data[1]),
        col=c('darkgoldenrod1'),
        border=NA,
        yaxt='n',
        xlim=c(0, ceiling(max(data[2:9])/5)*5),
        xlab='Load time(s)',
        cex.main=1.5)
barplot(t(as.matrix(data[9])),
        horiz=TRUE,
        names.arg=as.matrix(data[1]),
        col=c('darkslategray4'),
        border=NA,
        yaxt='n',
        xlim=c(0, ceiling(max(data[2:9])/5)*5),
        cex.main=1.5,
        add=TRUE)
barplot(t(as.matrix(data[8])),
        horiz=TRUE,
        names.arg=as.matrix(data[1]),
        col=c('darkslategray2'),
        border=NA,
        yaxt='n',
        xlim=c(0, ceiling(max(data[2:9])/5)*5),
        cex.main=1.5,
        add=TRUE)
barplot(t(as.matrix(data[7])),
        horiz=TRUE,
        names.arg=as.matrix(data[1]),
        col=c('goldenrod4'),
        border=NA,
        yaxt='n',
        xlim=c(0, ceiling(max(data[2:9])/5)*5),
        cex.main=1.5,
        add=TRUE)
barplot(t(as.matrix(data[6])),
        horiz=TRUE,
        names.arg=as.matrix(data[1]),
        col=c('darkgoldenrod1'),
        border=NA,
        yaxt='n',
        xlim=c(0, ceiling(max(data[2:9])/5)*5),
        cex.main=1.5,
        add=TRUE)
barplot(t(as.matrix(data[4])),
        horiz=TRUE,
        names.arg=as.matrix(data[1]),
        col=c('white'),
        border=NA,
        yaxt='n',
        xlim=c(0, ceiling(max(data[2:9])/5)*5),
        cex.main=1.5,
        add=TRUE)
barplot(t(as.matrix(data[3])),
        horiz=TRUE,
        names.arg=as.matrix(data[1]),
        col=c('gray'),
        border=NA,
        yaxt='n',
        xlim=c(0, ceiling(max(data[2:9])/5)*5),
        cex.main=1.5,
        add=TRUE)
barplot(t(as.matrix(data[2])),
        horiz=TRUE,
        names.arg=as.matrix(data[1]),
        col=c('white'),
        border=NA,
        yaxt='n',
        xlim=c(0, ceiling(max(data[2:9])/5)*5),
        cex.main=1.5,
        add=TRUE)

#barplot(t(as.matrix(data[2:9])), 
#        horiz=TRUE,
#        names.arg=as.matrix(data[1]),
#        col=c('white', 'gray', 'white', 'darkgoldenrod1', 'goldenrod4', 'darkslategray2', 'white', 'darkslategray4'),
#        border=NA,
#        yaxt='n',
#        xlim=c(0, 35),
#        xlab='Load time(s)',
#        cex.main=1.5)

labs = as.matrix(data[1])
text(x=0.25, 
     y=seq(0, length(as.matrix(data[1])))*1.19,
     labs)

legend(x="topright", inset = 0.015, 
       legend=c('DNS', 'Connect', 'SecureConnect', 
                'Request', 'Response'), 
       fill =c('gray', 'darkgoldenrod1', 'goldenrod4', 'darkslategray2', 'darkslategray4'))
#       legend=c('', 'DNS', '', 'Connect', 'SecureConnect', 
#                'Request', '', 'Response'), 
#       fill =c('white', 'gray', 'white', 'darkgoldenrod1', 'goldenrod4', 'darkslategray2', 'white', 'darkslategray4'))

par = temp_par
dev.off()
