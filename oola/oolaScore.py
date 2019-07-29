from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt


def oolaScore():
    false_positive_rate, true_positive_rate, thresholds = roc_curve(actual, predicts)
    roc_auc = auc(false_positive_rate, true_positive_rate)




    # Add OOLA text
    ax = plt.gca()
    textstr="Target: STUDENT ; FEATURES: Non-OOLA"

    ax.text(0.05, 0.05, textstr, transform=ax.transAxes, fontsize=14,
    verticalalignment='top')
    plt.plot(false_positive_rate, true_positive_rate, 'b',
    label='AUC = %0.2f'% roc_auc)
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc='lower right')
    plt.plot([0,1],[0,1],'r--')
    plt.xlim([-0.1,1.2])
    plt.ylim([-0.1,1.2])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()