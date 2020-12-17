import React from 'react';
import Modal from 'react-modal';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from 'react-router-dom';

import { fetchTreasureItems } from '../services/treasureItem';
import { fetchStudent } from '../services/student';
import { purchaseItem } from '../services/treasureItem';
import { studentLogout } from '../services/student';

import Passcode from '../pages/passcode';
import Welcome from '../pages/welcome';
import Shop from '../pages/shop';

import ItemModal from '../components/itemModal';

Modal.setAppElement('#root')

class App extends React.Component {
  constructor(props) {
    super(props);

    // Note this is usually an anti-pattern, but in this case it's okay. Properties coming into
    // this component is used as seed data. We do not expect props to ever change for this component.
    this.state = {
      students: props.students,
      currentStudent: props.currentStudent,
      treasureItems: props.treasureItems,
      selectedTreasureItem: {},
      isModalOpen: false,
    }

    this.makePurchase = this.makePurchase.bind(this);
    this.fetchShopItemsAndCurrentStudent = this.fetchShopItemsAndCurrentStudent.bind(this);
    this.onLogout = this.onLogout.bind(this);

    this.openPurchaseModal = this.openPurchaseModal.bind(this);
    this.closeModal = this.closeModal.bind(this);
  }

  openPurchaseModal(selectedTreasureItem) {
    document.body.style.overflow = 'hidden';

    this.setState({
      isModalOpen: true,
      selectedTreasureItem,
    })
  }

  closeModal() {
    document.body.style.overflow = 'auto';

    this.setState({
      isModalOpen: false,
      selectedTreasureItem: {},
    });
  }

  async fetchShopItemsAndCurrentStudent(studentId) {
    try {
      const [ treasureItemResult, currentStudentResult ] = await Promise.all([
        fetchTreasureItems(),
        fetchStudent(studentId)
      ]);

      this.setState({
        treasureItems: treasureItemResult.data.treasureItems,
        currentStudent: currentStudentResult.data.student
      });
    } catch(e) {
      console.log('an error occurred: ', e);
    }
  }

  async makePurchase(studentId, treasureItemId, onSuccess) {
    try {
      const result = await purchaseItem(studentId, treasureItemId);
      const { status, data } = result;
      if (status === 'success') {
        const { treasureItems, currentStudent } = this.state;

        const updatedTreasureItems = treasureItems.map((item) => {
          return item.id === data.treasure_item.id ?
            {...item, quantity: data.treasure_item.quantity} :
            item;
        });

        const updatedCurrentStudent = {
          ...currentStudent,
          points: data.student.points,
        }

        this.setState({
          treasureItems: updatedTreasureItems,
          currentStudent: updatedCurrentStudent
        });
        onSuccess();
      } else if (status === 'fail') {
        console.log('Purchase item failed ', result);
      }
    } catch (e) {
      console.log('an error occurred: ', e);
    }
  }

  async onLogout(history) {
    const result = await studentLogout();
    if (result.status === 'success') {
        history.replace('/');
        // clear session data
        this.setState({
          currentStudent: {},
          treasureItems: []
        });
    }
  }

  render() {
    const {
      authenticated,
      students,
      currentStudent,
      treasureItems,
      isModalOpen,
      selectedTreasureItem,
    } = this.state;

    const ShopWithProps = ({ history }) => {
      return (
        <Shop
          history={history}
          treasureItems={treasureItems}
          currentStudent={currentStudent}
          onLogout={() => this.onLogout(history)}
          onSelectItem={this.openPurchaseModal}
        />
      );
    };

    const PasscodeWithProps = ({ history }) => {
      return (
        <Passcode
          history={history}
          onSuccess={this.fetchShopItemsAndCurrentStudent}
        />
      );
    };

    return (
      <React.Fragment>
        <Router>
          <Switch>
              <Route path="/passcode" component={PasscodeWithProps}>
              </Route>
              <Route path="/shop" component={ShopWithProps}>
              </Route>
              <Route path="/">
                <Welcome users={students} />
              </Route>
          </Switch>
        </Router>
        <Modal
          isOpen={isModalOpen}
          contentLabel="Example Modal"
        >
          <ItemModal
            imageAlt={`${selectedTreasureItem.name} image`}
            imageSrc={selectedTreasureItem.image_path}
            title={selectedTreasureItem.name}
            subTitlePrimary={selectedTreasureItem.cost}
            primaryButtonLabel="Yes"
            secondaryButtonLabel="No"
            onPrimaryButtonClick={() => {
              this.makePurchase(
                currentStudent.id,
                selectedTreasureItem.id,
                this.closeModal,
              );
            }}
            onSecondaryButtonClick={this.closeModal}
          />
        </Modal>
      </React.Fragment>
    );
  }
}

export default App;